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

async def login_into_itsLearning() -> UserService:
    orgs_data = await Itslearning.search_organisations("Organisation Name")
    org = await Itslearning.fetch_organisation(orgs_data[0]["id"])
    return await org.login("Username", "Password")


async def setup():
    userService = await login_into_itsLearning()
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