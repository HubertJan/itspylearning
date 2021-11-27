# itspylearning

itspylearning is a fully async "It's Learning" API for Python. 
It can fetch organisations, log into user accounts and fetch information from these accounts like tasks or news.


## Getting Started

### Dependencies

* aiohttp

### Example

```Python
import asyncio

import itspylearning.itslearning as lib
from itspylearning.organisation import Organisation

async def setup():
    #Remember to change the login details.
    organisations = await lib.ItsLearning.searchOrganisations("Organisation Name")
    org: Organisation = await lib.ItsLearning.fetchOrganisation(organisations[0]["id"])
    user = await org.authenticate("Username", "Password")

    #It fetches all the tasks and outputs the name of the first task.
    tasks = await user.fetchTasks()
    print(tasks[0].name)

    #All sessions have to be closed.
    await lib.ItsLearning.closeSession()
    await org.closeSession()
    await user.closeSession()
    print("done")
    
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