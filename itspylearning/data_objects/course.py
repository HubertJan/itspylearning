from dataclasses import dataclass
from typing import Any

@dataclass
class Course:
    id: str
    name: str
    updated: str
    notificationCount: str
    newsCount: str
    url:str
    color:str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return Course(
            id= json['CourseId'],
            name= json['Title'],
            updated= json['LastUpdatedUtc'],
            notificationCount= json['NewNotificationsCount'],
            newsCount= json['NewBulletinsCount'],
            url= json['Url'],
            color= json['CourseColor']
        )
