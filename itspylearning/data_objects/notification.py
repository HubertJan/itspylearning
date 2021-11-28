from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.member import Member

@dataclass
class Notification:
    id:int
    text:str
    date:str
    author: Member
    type:str
    url:str
    content:str
    isRead:bool


    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  Any] = eval(json)
        return Notification(
            id= data['NotificationId'],
            text= data['Text'],
            date= data['PublishedDate'],
            author= Member(
                id= data['PublishedBy']['PersonId'],
                firstName= data['PublishedBy']['FirstName'],
                lastName= data['PublishedBy']['LastName'],
                profile= data['PublishedBy']['ProfileUrl'],
                profileImage= data['PublishedBy']['ProfileImageUrl']
            ),
            type= data['Type'],
            url= data['Url'],
            content= data['ContentUrl'],
            isRead= data['IsRead']
          )