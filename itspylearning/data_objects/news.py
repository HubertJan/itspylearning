from dataclasses import dataclass
from typing import Any, Optional


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
    content: Optional[Content]

    @staticmethod
    def fromFetchedJSON(json: Any):
        return News(
            id=json['NotificationId'],
            location=json['LocationTitle'],
            text=json['Text'],
            date=json['PublishedDate'],
            author=Member(
                id=json['PublishedBy']['PersonId'],
                first_name=json['PublishedBy']['FirstName'],
                last_name=json['PublishedBy']['LastName'],
                profile_url=json['PublishedBy']['ProfileUrl'],
                profile_image=json['PublishedBy']['ProfileImageUrl'],
                profile_image_small=json['PublishedBy']['ProfileImageUrlSmall'],
            ),
            type=json['ElementType'],
            url=json['Url'],
            content=Content(
                id=json["LightBulletin"]["LightBulletinId"],
                text=json["LightBulletin"]["Text"],
                url=json['ContentUrl']
            ) if json["LightBulletin"] else None
        )
