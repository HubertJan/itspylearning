# itspylearning

itspylearning is a fully async "It's Learning" API for Python. 
It can fetch organisations, log into user accounts and fetch information from these accounts like tasks or news.


## Getting Started

### Dependencies

* aiohttp

### Example

```Python
from itspylearning import *
import asyncio

async def loginIntoItsLearning() -> UserService:
    orgs_data = await Itslearning.search_organisations("Freie Hansestadt Bremen")
    org = await Itslearning.fetch_organisation(orgs_data[0]["id"])
    return await org.login("b-hubertjan1", "eindeutschersatz")


async def setup():
    userService = await loginIntoItsLearning()
    newsList = await userService.fetch_news()

    print(newsList[0])

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(setup())

```

## Contributing

Any contribution is welcome. If you can't code, but you have an idea for a feature, just post an issue.


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

It is inspired by the It's Learning API for Node JS.