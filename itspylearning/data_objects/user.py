from dataclasses import dataclass

from itspylearning.data_objects.member import Member


@dataclass
class User:
    member: Member
    language: str
    calender: str

    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return User(
            language=data['Language'],
            calender=data['iCalUrl'],
            member=Member(
                id=data['PersonId'],
                first_name=data['FirstName'],
                last_name=data['LastName'],
                profile_url=data['ProfileUrl'],
                profile_image=data['ProfileImageUrl'],
                profile_image_small=data['ProfileImageUrlSmall']
            ),
        )
