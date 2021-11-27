from dataclasses import dataclass
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

import itspylearning.organisation as org
import itspylearning.format_helper as helper

USER_AGENT = 'itslearningintapp/2.2.0 (com.itslearning.itslearningintapp; build:117; iOS 10.2.1) Alamofire/4.2.0'


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
    async def fetchUser(organisation, tokens: dict):
        client = User._createClient(id)
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

    async def fetchCourses(self) -> list[Course]:
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

    async def fetchTasks(self) -> list[Task]:
        data = await self._fetch("/restapi/personal/tasks/v1/")
        tasks: list[Task] = []

        for taskData in data["EntityArray"]:
            tasks.append(Task.fromFetchedJSON(taskData)),

        return tasks

    async def fetchNotifications(self) -> list[Notification]:
        data = await self._fetch("/restapi/personal/notifications/v1/", queryParameters={"PageIndex":0, "PageSize":20})
        notifications = []
        for notification in data["EntityArray"]:
            self.notifications.append(Notification.fromFetchedJSON(notification))

        return notifications

    async def fetchNews(self) -> list[News]:
        data = await self._fetch("/restapi/personal/notifications/stream/v1/", queryParameters={"PageIndex":0, "PageSize":20})
        news = []
        for newsData in data["EntityArray"]:
            news.append(News.fromFetchedJSON(newsData))

        return news
    
    async def fetchAllHierarchyMembersOfHierarchy(self, hierarchyId: int):
        
        pages = math.ceil(await self.fetchMemberCountOfHierarchy(hierarchyId) / 100)
        members = []

        for i in range(pages):
           members = members + await self.fetchHierarchyMembersOfHierarchy(hierarchyId, i)

        return members

    async def fetchHierarchy(self):
        data = await self._fetch(f"/restapi/personal/hierarchies/default/v1/")

        return Hierarchy.fromFetchedJSON(data)
    
    async def fetchMemberCountOfHierarchy(self, hierarchyId: int):
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex":100, "PageSize":0})

        return data["Total"]

    async def fetchHierarchyMembersOfHierarchy(self, hierarchyId: int, pageIndex: int):
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex":pageIndex})

        member = []
        for memberData in data["EntityArray"]:
            member.append(HierarchyMember.fromFetchedJSON(memberData))
        
        return member
    
    async def fetchCourseMemberList(self, hierarchyId: int):
        allHierarchyMembers = await self.fetchAllHierarchyMembersOfHierarchy(hierarchyId) 
        allHierarchyMembers : list(HierarchyMember)

        courseMembers = {}
        for hierarchyMember in allHierarchyMembers:
            sharedCourseNames = await self.fetchSharedCourseNames(hierarchyMember.member.id)
            if sharedCourseNames == None:
                continue
            for course in sharedCourseNames:
                if(not courseMembers.keys().__contains__(course)):
                    courseMembers[course] = []
                courseMembers[course].append(hierarchyMember.member)   
        
        return courseMembers
    
    async def fetchCourseStudentList(self, hierarchyId: int):
        allHierarchyMembers = await self.fetchAllHierarchyMembersOfHierarchy(hierarchyId) 
        allHierarchyMembers : list(HierarchyMember)

        courseMembers = {}
        for hierarchyMember in allHierarchyMembers:
            sharedCourseNames = await self.fetchSharedCourseNames(hierarchyMember.member.id)
            if sharedCourseNames == None:
                continue
            for course in sharedCourseNames:
                if(not courseMembers.keys().__contains__(course)):
                    courseMembers[course] = []
                if(hierarchyMember.hierarchyRole == "Schüler"):
                    courseMembers[course].append(hierarchyMember.member)   
        
        for courseName in courseMembers:
            courseMembers[courseName].append(self.member)

        return courseMembers
    
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
        return  self.ignoreTokenTimeout or self.accessToken and datetime.datetime.now() <= self.tokenTimeout

    @staticmethod
    def _createClient(id: str) -> aiohttp.ClientSession:
        return aiohttp.ClientSession(base_url="https://www.itslearning.com",  headers={
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