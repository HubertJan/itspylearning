from dataclasses import dataclass

@dataclass
class Member:
    id: str
    firstName: str
    lastName: str
    profile: str
    profileImage: str
    profileImageSmall: str
    
    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return Member(
            id=data['PersonId'],
            firstName=data['FirstName'],
            lastName=data['LastName'],
            profile=data['ProfileUrl'],
            profileImage=data['ProfileImageUrl'],
            profileImageSmall=data['ProfileImageUrlSmall']
        )