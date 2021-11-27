from dataclasses import dataclass

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


    def fromFetchedJSON(json: str):
        return Notification(
            id= json['NotificationId'],
            text= json['Text'],
            date= json['PublishedDate'],
            author= Member(
              id= json['PublishedBy']['PersonId'],
              firstName= json['PublishedBy']['FirstName'],
              lastName= json['PublishedBy']['LastName'],
              profile= json['PublishedBy']['ProfileUrl'],
              profileImage= json['PublishedBy']['ProfileImageUrl']
            ),
            type= json['Type'],
            url= json['Url'],
            content= json['ContentUrl'],
            isRead= json['IsRead']
          )