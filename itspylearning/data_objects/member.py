from dataclasses import dataclass
from typing import Any

@dataclass
class Member:
    id: str
    firstName: str
    lastName: str
    profile: str
    profileImage: str
    profileImageSmall: str
    
    @staticmethod
    def fromFetchedJSON(json: Any):
        return Member(
            id=json['PersonId'],
            firstName=json['FirstName'],
            lastName=json['LastName'],
            profile=json['ProfileUrl'],
            profileImage=json['ProfileImageUrl'],
            profileImageSmall=json['ProfileImageUrlSmall']
        )