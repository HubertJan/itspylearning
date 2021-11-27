import asyncio

import aiohttp
import json

import itspylearning.user as user
from typing import Final

#User agent for the It's Learning app
USER_AGENT = 'itslearningintapp/2.2.0 (com.itslearning.itslearningintapp; build:117; iOS 10.2.1) Alamofire/4.2.0'

#Id used across requests as client id of the It's Learning app
CLIENT_ID = '10ae9d30-1853-48ff-81cb-47b58a325685'

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
        return await user.User.fetchUser(self, data)

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


