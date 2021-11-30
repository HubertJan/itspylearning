from dataclasses import dataclass
from typing import Any

@dataclass
class Member:
    id: str
    first_name: str
    last_name: str
    profile_url: str
    profile_image: str
    profile_image_small: str
    
    @staticmethod
    def fromFetchedJSON(json: Any):
        return Member(
            id=json['PersonId'],
            first_name=json['FirstName'],
            last_name=json['LastName'],
            profile_url=json['ProfileUrl'],
            profile_image=json['ProfileImageUrl'],
            profile_image_small=json['ProfileImageUrlSmall']
        )