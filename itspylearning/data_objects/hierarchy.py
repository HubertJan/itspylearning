from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.content import Content

@dataclass
class Hierarchy:
    id: int
    parentId: int
    name: str
    path: str
    organisationType: str
    organisationHierarchyId: int

    @staticmethod
    def fromFetchedJSON(json: Any):
        return Hierarchy(
            id= json['HierarchyId'],
            parentId= json['ParentHierarchyId'],
            name= json['Title'],
            path= json['Path'],
            organisationType= json['OrganizationType'],
            organisationHierarchyId= json['OrganizationHierarchyId'],
        )
