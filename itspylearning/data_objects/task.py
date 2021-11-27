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

    def fromFetchedJSON(json: str):
        return Task(id=json['TaskId'],
                    name=json['Title'],
                    description=json['Description'],
                    courseName=json['LocationTitle'],
                    status=json['Status'],
                    deadline=json['Deadline'],
                    url=json['Url'],
                    content=json['ContentUrl'],
                    icon=json['IconUrl'],
                    elementId=json['ElementId'],
                    type=json['ElementType'],)
