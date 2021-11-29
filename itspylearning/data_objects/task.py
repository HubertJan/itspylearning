from dataclasses import dataclass
from typing import Any

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
    def fromFetchedJSON(json: Any):
        return Task(id=int(json['TaskId']),
                    name=json['Title'],
                    description=json['Description'],
                    courseName=json['LocationTitle'],
                    status=json['Status'],
                    deadline=json['Deadline'],
                    url=json['Url'],
                    content=json['ContentUrl'],
                    icon=json['IconUrl'],
                    elementId=int(json['ElementId']),
                    type=json['ElementType'],)
