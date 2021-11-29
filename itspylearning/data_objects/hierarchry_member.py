from dataclasses import dataclass

from itspylearning.data_objects.member import Member

@dataclass
class HierarchyMember:
    member: Member
    hierarchy_role: str
    additional_info: str

    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  str] = eval(json)
        return HierarchyMember(
            hierarchy_role=data['HierarchyRole'],
            additional_info=data['AdditionalInfo'],
            member=Member.fromFetchedJSON(json)
        )
