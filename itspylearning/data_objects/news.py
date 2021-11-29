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
    content: Content | None

    
    @staticmethod
    def fromFetchedJSON(data: Any):
        return News(
            id=data['NotificationId'],
            location=data['LocationTitle'],
            text=data['Text'],
            date=data['PublishedDate'],
            author=Member(
                id=data['PublishedBy']['PersonId'],
                first_name=data['PublishedBy']['FirstName'],
                last_name=data['PublishedBy']['LastName'],
                profile_url=data['PublishedBy']['ProfileUrl'],
                profile_image=data['PublishedBy']['ProfileImageUrl'],
                profile_image_small=data['PublishedBy']['ProfileImageUrlSmall'],
            ),
            type=data['ElementType'],
            url=data['Url'],
            content=   Content(
                id=data["LightBulletin"]["LightBulletinId"],
                text=data["LightBulletin"]["Text"],
                url=data['ContentUrl']
            ) if data["LightBulletin"] else None
        )
