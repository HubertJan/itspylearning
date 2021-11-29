from dataclasses import dataclass

@dataclass
class Member:
    id: str
    first_name: str
    last_name: str
    profile_url: str
    profile_image: str
    profile_image_small: str
    
    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return Member(
            id=data['PersonId'],
            first_name=data['FirstName'],
            last_name=data['LastName'],
            profile_url=data['ProfileUrl'],
            profile_image=data['ProfileImageUrl'],
            profile_image_small=data['ProfileImageUrlSmall']
        )