from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.member import Member


@dataclass
class User:
    member: Member
    language: str
    calender: str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return User(
            language=json['Language'],
            calender=json['iCalUrl'],
            member=Member(
                id=json['PersonId'],
                first_name=json['FirstName'],
                last_name=json['LastName'],
                profile_url=json['ProfileUrl'],
                profile_image=json['ProfileImageUrl'],
                profile_image_small=json['ProfileImageUrlSmall']
            ),
        )
