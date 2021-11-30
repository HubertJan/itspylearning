import asyncio
from datetime import datetime, timedelta
import aiohttp
import json

from attr import dataclass

from itspylearning.user_service import UserService
from typing import Final

from itspylearning.consts import USER_AGENT, CLIENT_ID


@dataclass
class LoginSessionData():
    access_token: str
    refresh_token: str
    token_timeout: datetime


class Organisation:
    def __init__(self, data):
        self.id: Final = data['CustomerId']
        self.name: Final = data['Title']
        self.short_name: Final = data['ShortName']
        self.url: Final = data['BaseUrl']
        self._session = None

    async def login(self, username, password) -> UserService:
        login_data = await self.re_login(username, password)
        return UserService(access_token=login_data.access_token,
                           refresh_token=login_data.refresh_token,
                           token_timeout=login_data.token_timeout,
                           organisation=self,
                           username=username,
                           password=password
                           )

    async def re_login(self, username, password) -> LoginSessionData:
        response = await self.session.post(f"/restapi/oauth2/token", data={"grant_type": "password", "client_id": CLIENT_ID, "password": password, "username": username})
        if response.status != 200:
            raise Exception('Request failure.')
        raw_data = await response.text()
        data = json.loads(raw_data)
        return LoginSessionData(access_token=data["access_token"],
                                refresh_token=data["refresh_token"],
                                token_timeout=datetime.now() +
                                timedelta(milliseconds=data['expires_in']), )

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close_session())
            else:
                loop.run_until_complete(self.close_session())
        except Exception:
            pass

    @property
    def session(self):
        if(self._session == None):
            self._session = aiohttp.ClientSession(base_url=self.url, headers={
                                                 "User-Agent": USER_AGENT,
                                                 "Content-Type": "application/x-www-form-urlencoded"},
                                                 cookies={
                                                     "login": f"CustomerId={self.id}"},
                                                 )
        return self._session

    async def close_session(self):
        if self.session == None:
            return
        await self.session.close()
        self._session = None
