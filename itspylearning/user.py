from typing import Callable, List, Union, TYPE_CHECKING

import aiohttp
import json
import datetime
import math

from itspylearning.data_objects.course import Course
from itspylearning.data_objects.hierarchry_member import HierarchyMember
from itspylearning.data_objects.hierarchy import Hierarchy
from itspylearning.data_objects.member import Member
from itspylearning.data_objects.news import News
from itspylearning.data_objects.notification import Notification
from itspylearning.data_objects.task import Task

from itspylearning.consts import USER_AGENT, ITSLEARNING_URL

if TYPE_CHECKING:
    from .organisation import Organisation

class User:
    def __init__(self,     accessToken: str,
                 refreshToken: str,
                 tokenTimeout: datetime.datetime,
                 organisation: object,
                 id: str,
                 firstName: str,
                 lastName: str,
                 language: str,
                 profileImage: str,
                 calendar: str,
                 client: aiohttp.client.ClientSession,):
        self.accessToken = accessToken
        self.refreshToken = refreshToken
        self.tokenTimeout = tokenTimeout
        self.organisation = organisation
        self.id = id
        self.firstName = firstName
        self.lastName = lastName
        self.language = language
        self.profileImage = profileImage
        self.calendar = calendar
        self._client = client
        self.ignoreTokenTimeout = False

    @staticmethod
    async def fetchUser(organisation: "Organisation", tokens: dict):
        client = User._createClient("")
        accessToken = tokens['access_token']
        response = await client.get(f"/restapi/personal/person/v1/?access_token={accessToken}#")

        if(response.status != 200):
            raise Exception('Request failure')
        rawData = await response.text()
        data = json.loads(rawData)

        return User(id=data['PersonId'],
                    firstName=data['FirstName'],
                    lastName=data['LastName'],
                    language=data['Language'],
                    profileImage=data['ProfileImageUrl'],
                    calendar=data['iCalUrl'],
                    accessToken=accessToken, client=client,
                    refreshToken=tokens['refresh_token'],
                    tokenTimeout=datetime.datetime.now(
        ) + datetime.timedelta(milliseconds=tokens['expires_in']),
            organisation=organisation,)

    async def fetchCourses(self) -> List[Course]:
        data = await self._fetch("/restapi/personal/courses/v1/")
        courses = []

        for course in data["EntityArray"]:
            courses.append(Course(id=course['CourseId'],
                                       name=course['Title'],
                                       updated=course['LastUpdatedUtc'],
                                       notificationCount=course['NewNotificationsCount'],
                                       newsCount=course['NewBulletinsCount'],
                                       url=course['Url'],
                                       color=course['CourseColor'],
                                       ),
                                )

        return courses

    async def fetchTasks(self) -> List[Task]:
        data = await self._fetch("/restapi/personal/tasks/v1/")
        tasks: list[Task] = []

        for taskData in data["EntityArray"]:
            tasks.append(Task.fromFetchedJSON(taskData))
        return tasks

    async def fetchNotifications(self) -> List[Notification]:
        data = await self._fetch("/restapi/personal/notifications/v1/", queryParameters={"PageIndex":0, "PageSize":20})
        notifications: List[Notification] = []
        for notification in data["EntityArray"]:
            notifications.append(Notification.fromFetchedJSON(notification))
        return notifications

    async def fetchNews(self) -> List[News]:
        data = await self._fetch("/restapi/personal/notifications/stream/v1/", queryParameters={"PageIndex":0, "PageSize":20})
        news = []
        for newsData in data["EntityArray"]:
            news.append(News.fromFetchedJSON(newsData))

        return news
    
    async def fetchAllHierarchyMembersOfHierarchy(self, hierarchyId: int ):
        pages = math.ceil(await self.fetchMemberCountOfHierarchy(hierarchyId) / 100)
        members: List[Member] = []

        for i in range(pages):
           members = members + await self.fetchHierarchyMembersOfHierarchy(hierarchyId, i)

        return members

    async def fetchHierarchy(self) -> Hierarchy:
        data = await self._fetch(f"/restapi/personal/hierarchies/default/v1/")

        return Hierarchy.fromFetchedJSON(data)
    
    async def fetchMemberCountOfHierarchy(self, hierarchyId: int) -> int:
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex":100, "PageSize":0})

        return data["Total"]

    async def fetchHierarchyMembersOfHierarchy(self, hierarchyId: int, pageIndex: int) -> List[Member]:
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex":pageIndex})

        member = []
        for memberData in data["EntityArray"]:
            member.append(HierarchyMember.fromFetchedJSON(memberData))
        
        return member

    async def sortMembersBySharedCourses(self, members: List[Union[Member, HierarchyMember] ], shouldBeAddToList: Callable[[Union[Member, HierarchyMember]], bool] = lambda _ : True) -> dict[str, List[Member]]:
        courseMembers: dict[str, List[Member]] = {}

        for member in members:
            if isinstance(member, HierarchyMember):
                memberData = member.member
            else:
                memberData = member
            sharedCourseNames = await self.fetchSharedCourseNames(memberData.id)
            if sharedCourseNames == None:
              continue
            for course in sharedCourseNames:
                if isinstance(course, Course):
                    courseName = course.name
                else:
                    courseName = course
                if not courseMembers.keys().__contains__(courseName):
                    courseMembers[courseName] = []
                if shouldBeAddToList(member):
                    courseMembers[courseName].append(memberData)
        return courseMembers
        
    
    # This is a workaround, if you have only access to a list of all members in your hierarchy
    # and you want to get a course member list
    async def fetchCourseMemberListThroughHierarchyList(self, hierarchyId: int | None = None, shouldBeAddToList: Callable[[Union[Member, HierarchyMember]], bool] = lambda _ : True):
        if(hierarchyId is None):
            hierarchyId = (await self.fetchHierarchy()).id
        members = await self.fetchAllHierarchyMembersOfHierarchy(hierarchyId)
        courseMemberList = await self.sortMembersBySharedCourses(members, shouldBeAddToList)
        return courseMemberList
    
    async def fetchSharedCourseNames(self, personId):
        data = await self._fetch(f"/restapi/personal/person/relations/{personId}/v1")
        if data == []:
            return []

        return data[0]["Items"]
    
    async def _fetch(self, url:str, queryParameters: dict = {}):
        if not self.isAuthenticated:
            raise Exception('Must be authenticated.')

        fullUrl = f"{url}?access_token={self.accessToken}"
        for key in queryParameters.keys():
            fullUrl = f"{fullUrl}&{key}={queryParameters[key]}"
        fullUrl = f"{fullUrl}#"

        response = await self.client.get(fullUrl)
        if(response.status != 200):
            raise Exception('Request failure')
        rawData = await response.text()
        return json.loads(rawData)
    
    @property
    def member(self):
        return Member(id= self.id, firstName=self.firstName, lastName=self.lastName, profile="", profileImageSmall= "", profileImage=self.profileImage,)

    @property
    def isAuthenticated(self) -> bool:
        return  self.ignoreTokenTimeout or self.accessToken != None and datetime.datetime.now() <= self.tokenTimeout

    @staticmethod
    def _createClient(id: str) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(base_url=ITSLEARNING_URL,  headers={
            "User-Agent": USER_AGENT}, cookies={"login": f"CustomerId={id}", },)

    @property
    def client(self):
        if(self._client == None):
            self._client = User._createClient(self.id)
        return self._client

    async def closeSession(self):
        if self._client == None:
            return
        await self._client.close()
        self._client = None