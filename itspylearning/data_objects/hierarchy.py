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
    def fromFetchedJSON(json: str):
        data: dict[str,  Any] = eval(json)
        return Hierarchy(
            id= data['HierarchyId'],
            parentId= data['ParentHierarchyId'],
            name= data['Title'],
            path= data['Path'],
            organisationType= data['OrganizationType'],
            organisationHierarchyId= data['OrganizationHierarchyId'],
        )
