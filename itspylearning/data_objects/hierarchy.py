from dataclasses import dataclass
from typing import Any

from itspylearning.data_objects.content import Content

@dataclass
class Hierarchy:
    id: int
    parent_id: int
    name: str
    path: str
    organisation_type: str
    organisation_hierarchy_id: int

    @staticmethod
    def fromFetchedJSON(json: str):
        data: dict[str,  Any] = eval(json)
        return Hierarchy(
            id= data['HierarchyId'],
            parent_id= data['ParentHierarchyId'],
            name= data['Title'],
            path= data['Path'],
            organisation_type= data['OrganizationType'],
            organisation_hierarchy_id= data['OrganizationHierarchyId'],
        )
