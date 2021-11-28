import aiohttp
import json

from aiohttp.client import ClientSession

import itspylearning.consts as _consts
import itspylearning.organisation as _org

_clientSession: ClientSession| None = None

def _getClient() -> aiohttp.ClientSession:
    global _clientSession
    if(_clientSession is None):
        _clientSession = aiohttp.ClientSession(base_url=_consts.ITSLEARNING_URL)
    return  _clientSession

async def searchOrganisations(query) -> list[dict]:
    response = await _getClient().get(f"/restapi/sites/all/organisations/search/v1/?searchText={query}")
    rawData = await response.text()
    data = json.loads(rawData)
    matches = []
    for match in data["EntityArray"]:
        matches.append({"id": match["CustomerId"], "name": match["SiteName"],})
    return matches

async def fetchOrganisation( id) -> _org.Organisation:
    response = await _getClient().get(f"/restapi/sites/{id}/v1")
    if response.status != 200:
        raise Exception('Request failure.')
    rawData = await response.text()
    data = json.loads(rawData)
    if data == None:
        raise Exception("Organisation did not exist.")
    organisation = _org.Organisation(data)
    return organisation


async def closeSession():
    global _clientSession
    await _clientSession.close()
    _clientSession = None