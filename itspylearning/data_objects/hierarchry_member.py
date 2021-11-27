from dataclasses import dataclass

from itspylearning.data_objects.member import Member


@dataclass
class HierarchyMember:
    member: Member
    hierarchyRole: str
    additionalInfo: str

    def fromFetchedJSON(json: str):
        return HierarchyMember(
            hierarchyRole=json['HierarchyRole'],
            additionalInfo=json['AdditionalInfo'],
            member=Member.fromFetchedJSON(json)
        )
