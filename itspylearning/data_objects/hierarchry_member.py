from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.member import Member

@dataclass
class HierarchyMember:
    member: Member
    hierarchy_role: str
    additional_info: str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return HierarchyMember(
            hierarchy_role=json['HierarchyRole'],
            additional_info=json['AdditionalInfo'],
            member=Member.fromFetchedJSON(json)
        )
