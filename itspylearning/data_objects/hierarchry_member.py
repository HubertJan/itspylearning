from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.member import Member

@dataclass
class HierarchyMember:
    member: Member
    hierarchyRole: str
    additionalInfo: str

    @staticmethod
    def fromFetchedJSON(json: Any):
        return HierarchyMember(
            hierarchyRole=json['HierarchyRole'],
            additionalInfo=json['AdditionalInfo'],
            member=Member.fromFetchedJSON(json)
        )
