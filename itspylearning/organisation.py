import aiohttp
import json

from itspylearning.user import User
from typing import Final

from itspylearning.consts import USER_AGENT, CLIENT_ID

class Organisation:
    def __init__(self, data):
        self.id: Final = data['CustomerId']
        self.name: Final = data['Title']
        self.shortName: Final = data['ShortName']
        self.url: Final = data['BaseUrl']
        self._client = None

    async def authenticate(self, username, password):
        response = await self.client.post(f"/restapi/oauth2/token", data={"grant_type": "password","client_id": CLIENT_ID, "password": password, "username": username})
        if response.status != 200:
            raise Exception('Request failure.')
        rawData = await response.text()
        data = json.loads(rawData)
        return await User.fetchUser(self, data)

    @property
    def client(self):
        if(self._client == None):
            self._client =  aiohttp.ClientSession(base_url=self.url, headers= {"User-Agent": USER_AGENT,"Content-Type": "application/x-www-form-urlencoded"},cookies={"login": f"CustomerId={self.id}"})
        return self._client
    
    async def closeSession(self):
        if self.client == None:
            return
        await self.client.close()
        self._client = None


