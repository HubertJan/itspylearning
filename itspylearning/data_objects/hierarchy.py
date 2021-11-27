from dataclasses import dataclass

from itspylearning.data_objects.content import Content

@dataclass
class Hierarchy:
    id: int
    parentId: int
    name: str
    path: str
    organisationType: str
    organisationHierarchyId: int

    def fromFetchedJSON(json: str):
        return Hierarchy(
            id= json['HierarchyId'],
            parentId= json['ParentHierarchyId'],
            name= json['Title'],
            path= json['Path'],
            organisationType= json['OrganizationType'],
            organisationHierarchyId= json['OrganizationHierarchyId'],
        )
