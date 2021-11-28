from dataclasses import dataclass

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
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return Course(
            id= data['CourseId'],
            name= data['Title'],
            updated= data['LastUpdatedUtc'],
            notificationCount= data['NewNotificationsCount'],
            newsCount= data['NewBulletinsCount'],
            url= data['Url'],
            color= data['CourseColor']
        )
