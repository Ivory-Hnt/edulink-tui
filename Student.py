import json
from datetime import datetime

import requests


class Student:
    def __init__(self):
        # School information dictionary, contains stuff like the provisioning (school server) URL
        self.school: dict = None

        # Our Authentication Token
        self.authentication: str = None

        # Dictionary containing information about ourselves as a studnet. has stuff like student id, etc
        self.learner: dict = None

    def customrequest(
        self,
        request_type: str,
        provision_url: str,
        method: str,
        headers: dict = None,
        params: dict = None,
    ):
        # 'is' operator specifically compares object identity, rather than value equality like '=='
        if headers is None:
            headers = {}
        if params is None:
            params = {}

        payload = json.dumps(
            {"id": "1", "jsonrpc": "2.0", "method": method, "params": params}
        )

        headers["Content-Type"] = "application/json;charset=UTF-8"
        # calculating content length is unnecessary when using Python's requests library, unlike coro-http in Lua
        # headers["Content-Length"] = str(len(payload))
        headers["X-Api-Method"] = method

        if self.authentication:
            headers["Authorization"] = f"Bearer {self.authentication}"

        params["method"] = method

        response = requests.request(
            request_type,
            provision_url,
            params=params,
            headers=headers,
            data=payload,
        )

        body = response.json()
        if not body or not body.get("result", {}).get("success"):
            errmsg = body.get("result", {}).get(
                "error", "No error was provided by the EduLink API."
            )
            raise Exception(
                f"Error in request, returned HTTP {response.status_code} with API Response: {errmsg}"
            )

        return body["result"]

    def provision(self, school_postcode: str):
        result = self.customrequest(
            "POST",
            "https://provisioning.edulinkone.com/",
            "School.FromCode",
            params={"code": school_postcode},
        )

        # We dont care about errors here because all errors are handled in customrequest()
        self.school = result.get("school")

        return self.school

    def authenticate(self, username: str, password: str, school_postcode: str = None) -> str:
        if not school_postcode and not self.school:
            raise Exception(
                "Neither the school postcode or an existing school information dictionary were available. Authentication failed due to lack of information."
            )

        self.school = self.school or self.provision(school_postcode)

        result = self.customrequest(
            "POST",
            self.school["server"],
            "EduLink.Login",
            # silly EduLink sending passwords over clear text! in the query string parameters too!
            # any web browser extension which can read your requests will simply see your credentials without having to dig deeper into the request content, headers, etc.
            params={
                "establishment_id": self.school["school_id"],
                "username": username,
                "password": password,
                "from_app": False,
            },
        )

        self.authentication = result.get("authtoken")
        self.learner = result.get("user")

        return self.authentication

    # merged timetable() and timetable_week() into one function. use time_scale parameter instead.
    def timetable(
        self,
        time_scale: str = "day",
        date=None,
        # "exact" returns data for the EXACT specified data and raises an error if none is found for the EXACT date.
        # "close" will return data found for the specified date or return data for the closest future date without raising errors.
        proximity: str = "exact",
        learner_id: int = None,
    ) -> dict:
        if time_scale not in ["day", "week"]:
            raise ValueError(
                f"{time_scale} is not a valid time scale. time_scale can only be 'day' or 'week'."
            )

        if proximity not in ["exact", "close"]:
            raise ValueError(
                f"{proximity} is not a valid proximity. proximity can only be 'exact' or 'close'."
            )

        # Provide support for both a UNIX timestamp and regular python date classes
        date = date or int(datetime.now().timestamp())
        if isinstance(date, int):
            date = datetime.fromtimestamp(date).strftime("%Y-%m-%d")

        learner_id = learner_id or self.learner["id"]

        result = self.customrequest(
            "POST",
            self.school["server"],
            "EduLink.Timetable",
            params={"learner_id": learner_id, "date": date},
        )

        # TODO: implement close proximity support later
        if time_scale == "week":
            return result.get("weeks")
        elif time_scale == "day":
            found = None
            for week in result.get("weeks", []):
                for day in week.get("days", []):
                    if day["date"] == date:
                        found = day.get("lessons")
                        break

            if not found:
                raise Exception("No timetable data was found for the EXACT date.")

            return found

    def homework(self, learner_id: int = None) -> dict:
        learner_id = learner_id or self.learner["id"]

        result = self.customrequest(
            "POST", self.school["server"], "EduLink.Homework", params={"format": 2}
        )

        return result["homework"]

    def homeworkInfo(
        self, homework_id: str, homework_source: str = "EduLink", learner_id: int = None
    ) -> dict:
        learner_id = learner_id or self.learner["id"]

        result = self.customrequest(
            "POST",
            self.school["server"],
            "EduLink.HomeworkDetails",
            params={"homework_id": homework_id, "source": homework_source},
        )

        return result["homework"]
