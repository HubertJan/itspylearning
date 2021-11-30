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
    def fromFetchedJSON(json: Any):
        return Hierarchy(
            id= json['HierarchyId'],
            parent_id= json['ParentHierarchyId'],
            name= json['Title'],
            path= json['Path'],
            organisation_type= json['OrganizationType'],
            organisation_hierarchy_id= json['OrganizationHierarchyId'],
        )
