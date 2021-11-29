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
                first_name= data['PublishedBy']['FirstName'],
                last_name= data['PublishedBy']['LastName'],
                profile_url= data['PublishedBy']['ProfileUrl'],
                profile_image= data['PublishedBy']['ProfileImageUrl'],
                profile_image_small= data['PublishedBy']['ProfileImageUrlSmall'] 
            ),
            type= data['Type'],
            url= data['Url'],
            content= data['ContentUrl'],
            isRead= data['IsRead']
          )