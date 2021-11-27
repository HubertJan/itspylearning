from dataclasses import dataclass

@dataclass

class Member:
    id: str
    firstName: str
    lastName: str
    profile: str
    profileImage: str
    profileImageSmall: str

    def fromFetchedJSON(json: str):
        return Member(
            id=json['PersonId'],
            firstName=json['FirstName'],
            lastName=json['LastName'],
            profile=json['ProfileUrl'],
            profileImage=json['ProfileImageUrl'],
            profileImageSmall=json['ProfileImageUrlSmall']
        )