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
    def fromFetchedJSON(json: Any):
        return Notification(
            id= json['NotificationId'],
            text= json['Text'],
            date= json['PublishedDate'],
            author= Member(
                id= json['PublishedBy']['PersonId'],
                firstName= json['PublishedBy']['FirstName'],
                lastName= json['PublishedBy']['LastName'],
                profile= json['PublishedBy']['ProfileUrl'],
                profileImage= json['PublishedBy']['ProfileImageUrl'],
                profileImageSmall= json['PublishedBy']['ProfileImageUrlSmall'] 
            ),
            type= json['Type'],
            url= json['Url'],
            content= json['ContentUrl'],
            isRead= json['IsRead']
          )