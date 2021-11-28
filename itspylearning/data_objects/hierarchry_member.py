from dataclasses import dataclass

from itspylearning.data_objects.member import Member

@dataclass
class HierarchyMember:
    member: Member
    hierarchyRole: str
    additionalInfo: str

    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return HierarchyMember(
            hierarchyRole=data['HierarchyRole'],
            additionalInfo=data['AdditionalInfo'],
            member=Member.fromFetchedJSON(json)
        )
