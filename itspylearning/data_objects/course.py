from dataclasses import dataclass

from itspylearning.data_objects.content import Content

@dataclass
class Course:
    id: str
    name: str
    updated: str
    notificationCount: str
    newsCount: str
    url:str
    color:str

    def fromFetchedJSON(json: str):
        return Course(
            id= json['CourseId'],
            name= json['Title'],
            updated= json['LastUpdatedUtc'],
            notificationCount= json['NewNotificationsCount'],
            newsCount= json['NewBulletinsCount'],
            url= json['Url'],
            color= json['CourseColor']
        )
