from dataclasses import dataclass

@dataclass
class Task:
    id: int
    name: str
    description: str
    courseName: str
    status: str
    deadline: str
    url: str
    content: str
    icon: str
    elementId: int
    type: str

    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return Task(id=int(data['TaskId']),
                    name=data['Title'],
                    description=data['Description'],
                    courseName=data['LocationTitle'],
                    status=data['Status'],
                    deadline=data['Deadline'],
                    url=data['Url'],
                    content=data['ContentUrl'],
                    icon=data['IconUrl'],
                    elementId=int(data['ElementId']),
                    type=data['ElementType'],)
