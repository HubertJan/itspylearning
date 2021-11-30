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
<<<<<<< HEAD
=======
<<<<<<< Updated upstream
            id= data['HierarchyId'],
            parent_id= data['ParentHierarchyId'],
            name= data['Title'],
            path= data['Path'],
            organisation_type= data['OrganizationType'],
            organisation_hierarchy_id= data['OrganizationHierarchyId'],
=======
>>>>>>> build
            id= json['HierarchyId'],
            parentId= json['ParentHierarchyId'],
            name= json['Title'],
            path= json['Path'],
<<<<<<< HEAD
            organisationType= json['OrganizationType'],
            organisationHierarchyId= json['OrganizationHierarchyId'],
=======
            organisation_type= json['OrganizationType'],
            organisation_hierarchy_id= json['OrganizationHierarchyId'],
>>>>>>> Stashed changes
>>>>>>> build
        )
