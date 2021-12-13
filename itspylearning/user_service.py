import asyncio
from typing import Any, Callable, List, Optional, Union, TYPE_CHECKING, Dict

import aiohttp
import json
import datetime
import math

from aiohttp.client import ClientSession

from itspylearning.data_objects.course import Course
from itspylearning.data_objects.hierarchry_member import HierarchyMember
from itspylearning.data_objects.hierarchy import Hierarchy
from itspylearning.data_objects.member import Member
from itspylearning.data_objects.news import News
from itspylearning.data_objects.notification import Notification
from itspylearning.data_objects.task import Task

from itspylearning.consts import USER_AGENT, ITSLEARNING_URL
from itspylearning.data_objects.user import User
import itspylearning.organisation as org

if TYPE_CHECKING:
    from .organisation import Organisation


class UserService:
    def __init__(self,
                 access_token: str,
                 refresh_token: str,
                 token_timeout: datetime.datetime,
                 organisation: "Organisation",
                 username: str,
                 password: str,
                 ):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.token_timeout = token_timeout
        self.organisation = organisation
        self.ignore_token_timeout = False
        self.username = username
        self.password = password
        self._session: Optional[ClientSession] = None

    async def fetch_user(self):
        data = await self._fetch("/restapi/personal/courses/v1/")
        return User(data)

    async def fetch_courses(self) -> List[Course]:
        data = await self._fetch("/restapi/personal/courses/v1/")
        courses = []

        for course in data["EntityArray"]:
            courses.append(Course(id=course['CourseId'],
                                  name=course['Title'],
                                  updated=course['LastUpdatedUtc'],
                                  notification_count=course['NewNotificationsCount'],
                                  news_count=course['NewBulletinsCount'],
                                  url=course['Url'],
                                  color=course['CourseColor'],
                                  ),
                           )
        return courses

    async def fetch_tasks(self) -> List[Task]:
        data = await self._fetch("/restapi/personal/tasks/v1/")
        tasks: List[Task] = []

        for taskData in data["EntityArray"]:
            tasks.append(Task.fromFetchedJSON(taskData))
        return tasks

    async def fetch_notifications(self) -> List[Notification]:
        data = await self._fetch("/restapi/personal/notifications/v1/", queryParameters={"PageIndex": 0, "PageSize": 20})
        notifications: List[Notification] = []
        for notification in data["EntityArray"]:
            notifications.append(Notification.fromFetchedJSON(notification))
        return notifications

    async def fetch_news(self) -> List[News]:
        data = await self._fetch("/restapi/personal/notifications/stream/v1/", queryParameters={"PageIndex": 0, "PageSize": 20})
        news = []
        for newsData in data["EntityArray"]:
            news.append(News.fromFetchedJSON(newsData))

        return news

    async def fetch_all_hierarchy_members_of_hierarchy(self, hierarchyId: int) -> List[HierarchyMember]:
        pages = math.ceil(await self.fetch_member_count_of_hierarchy(hierarchyId) / 100)
        members: List[HierarchyMember] = []

        for i in range(pages):
            members = members + await self.fetch_hierarchy_members_of_hierarchy(hierarchyId, i)

        return members

    async def fetch_hierarchy(self) -> Hierarchy:
        data = await self._fetch(f"/restapi/personal/hierarchies/default/v1/")

        return Hierarchy.fromFetchedJSON(data)

    async def fetch_member_count_of_hierarchy(self, hierarchyId: int) -> int:
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex": 100, "PageSize": 0})

        return data["Total"]

    async def fetch_hierarchy_members_of_hierarchy(self, hierarchyId: int, pageIndex: int) -> List[HierarchyMember]:
        data = await self._fetch(f"/restapi/personal/hierarchies/{hierarchyId}/members/v1/", queryParameters={"PageIndex": pageIndex})

        member = []
        for memberData in data["EntityArray"]:
            member.append(HierarchyMember.fromFetchedJSON(memberData))

        return member

    async def sort_members_by_shared_courses(self, members:Union[ List[HierarchyMember] , List[Union [Member , HierarchyMember]] ],
                                             shouldBeAddToList: Callable[[Union [Member , HierarchyMember]], bool] = lambda _: True) -> Dict[str, List[Union [Member , HierarchyMember]]]:
        courseMembers: Dict[str, List[Union [Member , HierarchyMember]]] = {}

        for member in members:
            if isinstance(member, HierarchyMember):
                memberData = member.member
            else:
                memberData = member
            sharedCourseNames = await self.fetch_shared_course_names(memberData.id)
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

    async def fetch_course_member_list_by_hierarchy_list(self, hierarchyId: Optional[int] = None,
                                                         shouldBeAddToList: Callable[[Union[Member, HierarchyMember]], bool] = lambda _: True) -> Dict[str, List[Union[HierarchyMember , Member]]]:
        if(hierarchyId is None):
            hierarchyId = (await self.fetch_hierarchy()).id
        members = await self.fetch_all_hierarchy_members_of_hierarchy(hierarchyId)
        courseMemberList = await self.sort_members_by_shared_courses(members, shouldBeAddToList)
        return courseMemberList

    async def fetch_shared_course_names(self, personId):
        data = await self._fetch(f"{ITSLEARNING_URL}/restapi/personal/person/relations/{personId}/v1")
        if data == []:
            return []

        return data[0]["Items"]

    async def _fetch(self, url: str, queryParameters: dict = {}) -> Any:
        if not self.is_authenticated:
            await self.authenticate()
            if not self.is_authenticated:
                raise Exception('Must be authenticated.')

        fullUrl = f"{ITSLEARNING_URL}/{url}?access_token={self.access_token}"
        for key in queryParameters.keys():
            fullUrl = f"{fullUrl}&{key}={queryParameters[key]}"
        fullUrl = f"{fullUrl}#"

        response = await self.client.get(fullUrl)
        if(response.status != 200):
            raise Exception('Request failure')
        rawData = await response.text()
        return json.loads(rawData)

    async def authenticate(self) -> None:
        new_login_data = await self.organisation.re_login(self.username, self.password)
        self.access_token = new_login_data.access_token
        self.refresh_token = new_login_data.refresh_token
        self.token_timeout = new_login_data.token_timeout

    @property
    def member(self):
        return Member(id=self.id, first_name=self.first_name, last_name=self.last_name, profile_url="", profile_image_small="", profile_image=self.profile_image,)

    @property
    def is_authenticated(self) -> bool:
        return self.ignore_token_timeout or self.access_token != None and datetime.datetime.now() <= self.token_timeout

    @staticmethod
    def _create_session() -> aiohttp.ClientSession:
        return aiohttp.ClientSession(  headers={
            "User-Agent": USER_AGENT},)

    def __del__(self):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close_session())
            else:
                loop.run_until_complete(self.close_session())
        except Exception:
            pass

    async def close_session(self):
        if self._session is None:
            return
        await self._session.close()
        self._session = None

    @property
    def client(self) -> ClientSession:
        if self._session is None:
            self._session = UserService._create_session()
        return self._session
