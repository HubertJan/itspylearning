from dataclasses import dataclass

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
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return Course(
            id= data['CourseId'],
            name= data['Title'],
            updated= data['LastUpdatedUtc'],
            notification_count= data['NewNotificationsCount'],
            news_count= data['NewBulletinsCount'],
            url= data['Url'],
            color= data['CourseColor']
        )
