import aiohttp
import json

from aiohttp.client import ClientSession

from itspylearning.consts import ITSLEARNING_URL
from itspylearning.organisation import Organisation

_clientSession: ClientSession| None = None

def _getClient() -> aiohttp.ClientSession:
    global _clientSession
    if(_clientSession is None):
        _clientSession = aiohttp.ClientSession(base_url=ITSLEARNING_URL)
    return  _clientSession

async def search_organisations(query) -> list[dict]:
    response = await _getClient().get(f"/restapi/sites/all/organisations/search/v1/?searchText={query}")
    rawData = await response.text()
    data = json.loads(rawData)
    matches = []
    for match in data["EntityArray"]:
        matches.append({"id": match["CustomerId"], "name": match["SiteName"],})
    await close_session()
    return matches

async def fetch_organisation( id) -> Organisation:
    response = await _getClient().get(f"/restapi/sites/{id}/v1")
    if response.status != 200:
        raise Exception('Request failure.')
    rawData = await response.text()
    data = json.loads(rawData)
    if data == None:
        raise Exception("Organisation did not exist.")
    organisation = Organisation(data)
    await close_session()
    return organisation


async def close_session():
    global _clientSession
    await _clientSession.close()
    _clientSession = None