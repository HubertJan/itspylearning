from dataclasses import dataclass
from typing import Any


from itspylearning.data_objects.content import Content
from itspylearning.data_objects.member import Member


@dataclass
class News:
    id: str
    location: str
    text: str
    date: str
    author: Member
    type: str
    url: str
    content: Content

    
    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str, Any] = eval(json)
        return News(
            id=data['NotificationId'],
            location=data['LocationTitle'],
            text=data['Text'],
            date=data['PublishedDate'],
            author=Member(
                id=data['PublishedBy']['PersonId'],
                firstName=data['PublishedBy']['FirstName'],
                lastName=data['PublishedBy']['LastName'],
                profile=data['PublishedBy']['ProfileUrl'],
                profileImage=data['PublishedBy']['ProfileImageUrl']
            ),
            type=data['ElementType'],
            url=data['Url'],
            content=Content(
                id=None,
                text=None,
                url=data['ContentUrl']
            )
        )
