import aiohttp
import json

import itspylearning.organisation as org

USER_AGENT = 'itslearningintapp/2.2.0 (com.itslearning.itslearningintapp; build:117; iOS 10.2.1) Alamofire/4.2.0'



class ItsLearning:
    _clientSession = None

    __single = None
    def __init__( self ):
        if ItsLearning.__single:
            raise ItsLearning.__single
        ItsLearning.__single = self

    async def searchOrganisations(self,query) -> list[dict]:
        response = await self._client.get(f"/restapi/sites/all/organisations/search/v1/?searchText={query}")
        rawData = await response.text()
        data = json.loads(rawData)
        matches = []
        for match in data["EntityArray"]:
            matches.append({"id": match["CustomerId"], "name": match["SiteName"],})
        return matches
    
    async def fetchOrganisation(self, id) -> org.Organisation:
        response = await self._client.get(f"/restapi/sites/{id}/v1")
        if response.status != 200:
            raise Exception('Request failure.')
        rawData = await response.text()
        data = json.loads(rawData)
        if data == None:
            raise Exception("Organisation did not exist.")
        organisation = org.Organisation(data)
        return organisation

    @property
    def _client(self):
        if(self._clientSession == None):
            ItsLearning._clientSession = aiohttp.ClientSession(base_url='https://www.itslearning.com')
        return  ItsLearning._clientSession
    
    async def closeSession(self):
        await self._clientSession.close()
        ItsLearning._clientSession = None
    

ItsLearning = ItsLearning()