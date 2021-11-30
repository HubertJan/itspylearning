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
    is_read:bool


    @staticmethod
    def fromFetchedJSON(json: Any):
        return Notification(
            id= json['NotificationId'],
            text= json['Text'],
            date= json['PublishedDate'],
            author= Member(
                id= json['PublishedBy']['PersonId'],
                first_name= json['PublishedBy']['FirstName'],
                last_name= json['PublishedBy']['LastName'],
                profile_url= json['PublishedBy']['ProfileUrl'],
                profile_image= json['PublishedBy']['ProfileImageUrl'],
                profile_image_small= json['PublishedBy']['ProfileImageUrlSmall'] 
            ),
            type= json['Type'],
            url= json['Url'],
            content= json['ContentUrl'],
            is_read= json['IsRead']
          )