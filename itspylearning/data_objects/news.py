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
    def fromFetchedJSON(json: Any):
        return News(
            id=json['NotificationId'],
            location=json['LocationTitle'],
            text=json['Text'],
            date=json['PublishedDate'],
            author=Member(
                id=str(json['PublishedBy']['PersonId']),
                firstName=str(json['PublishedBy']['FirstName']),
                lastName=str(json['PublishedBy']['LastName']),
                profile=str(json['PublishedBy']['ProfileUrl']),
                profileImage=str(json['PublishedBy']['ProfileImageUrl']),
                profileImageSmall=""
            ),
            type=json['ElementType'],
            url=json['Url'],
            content= Content(
                id=json["LightBulletin"]["LightBulletinId"],
                text=json["LightBulletin"]["Text"],
                url=json['ContentUrl']
            ) if json["LightBulletin"] else None
        )
