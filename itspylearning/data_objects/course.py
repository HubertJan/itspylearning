from dataclasses import dataclass
from typing import Any

@dataclass
class Course:
    id: str
    name: str
    updated: str
    notification_count: str
    news_count: str
    url:str
    color:str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return Course(
            id= json['CourseId'],
            name= json['Title'],
            updated= json['LastUpdatedUtc'],
            notification_count= json['NewNotificationsCount'],
            news_count= json['NewBulletinsCount'],
            url= json['Url'],
            color= json['CourseColor']
        )
