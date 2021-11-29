from dataclasses import dataclass
from typing import Any

@dataclass
class Task:
    id: int
    name: str
    description: str
    course_name: str
    status: str
    deadline: str
    url: str
    content: str
    icon: str
    element_id: int
    type: str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return Task(id=int(json['TaskId']),
                    name=json['Title'],
                    description=json['Description'],
                    course_name=json['LocationTitle'],
                    status=json['Status'],
                    deadline=json['Deadline'],
                    url=json['Url'],
                    content=json['ContentUrl'],
                    icon=json['IconUrl'],
                    element_id=int(json['ElementId']),
                    type=json['ElementType'],)
