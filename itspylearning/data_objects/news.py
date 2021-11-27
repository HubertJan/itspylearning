from dataclasses import dataclass


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

    def fromFetchedJSON(json: str):
        return News(
            id=json['NotificationId'],
            location=json['LocationTitle'],
            text=json['Text'],
            date=json['PublishedDate'],
            author=Member(
                id=json['PublishedBy']['PersonId'],
                firstName=json['PublishedBy']['FirstName'],
                lastName=json['PublishedBy']['LastName'],
                profile=json['PublishedBy']['ProfileUrl'],
                profileImage=json['PublishedBy']['ProfileImageUrl']
            ),
            type=json['ElementType'],
            url=json['Url'],
            content=Content(
                id=None,
                text=None,
                url=json['ContentUrl']
            )
        )
