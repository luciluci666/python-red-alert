# -*- coding: utf-8 -*-
#!/usr/bin/python

import random
import math
import requests
import json
import time


class RedAlert:
    def __init__(self):
        # initialize locations list
        self.locations = self.get_locations_list()
        # cookies
        self.cookies = ""
        # initialize user agent for web requests
        self.headers = {
            "Host": "www.oref.org.il",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "charset": "utf-8",
            "X-Requested-With": "XMLHttpRequest",
            "sec-ch-ua-mobile": "?0",
            "User-Agent": "",
            "sec-ch-ua-platform": "macOS",
            "Accept": "*/*",
            "sec-ch-ua": '".Not/A)Brand"v="99", "Google Chrome";v="103", "Chromium";v="103"',
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.oref.org.il/12481-he/Pakar.aspx",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        }
        # intiiate cokies
        self.get_cookies()

    def get_cookies(self):
        HOST = "https://www.oref.org.il/"
        r = requests.get(HOST, headers=self.headers)
        self.cookies = r.cookies

    def get_coordinates(self, location_name):
        # This function will get city coordinates by given city name
        # so later on it will be possible to visualization the flying rocket to the city
        HOST = (
            "https://maps.google.com/maps/api/geocode/json?address=%s" % location_name
        )
        r = requests.get(HOST, headers=self.headers)
        j = json.loads(r.content)
        return j["results"][0]["geometry"]["location"]

    def random_coordinates(self, latitude, longitude):
        # get random coordinates within the city for random visualization
        # radius of the circle
        circle_r = 1
        # center of the circle (x, y)
        circle_x = latitude
        circle_y = longitude
        # random angle
        alpha = 2 * math.pi * random.random()
        # random radius
        r = circle_r * random.random()
        # calculating coordinates
        x = r * math.cos(alpha) + circle_x
        y = r * math.sin(alpha) + circle_y
        return {"latitude": x, "longitude": y}

    def count_alerts(self, alerts_data):
        # this function literally return how many alerts there are currently
        return len(alerts_data)

    def get_locations_list(self):
        """
        This function is to build a locations list of cities and the time they have
        before the rocket hit the fan. for better parsing later
        """

        f = open("resources/targets.json", encoding="utf-8")
        # returns JSON object as
        return json.load(f)

    def get_red_alerts_history(self, lang="en", mode=1, from_date=None, to_date=None):
        """
        lang:
        en - english
        ru - russian
        he - hebrew

        mode:
        0 - all alerts; fromDate and toDate are mandatory; format 18.01.2025
        1 - today alerts;
        2 - week alerts;
        3 - month alerts;

        from_date: format 18.01.2025
        to_date: format 18.01.2025
        """
        # HOST = "https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang=ru&mode=1"
        HOST = f"https://alerts-history.oref.org.il//Shared/Ajax/GetAlarmsHistory.aspx?lang={lang}&mode={mode}{f'&fromDate={from_date}&toDate={to_date}' if mode == 0 else ''}"
        r = requests.get(
            HOST,
            headers={
                "accept": "*/*",
                "accept-language": "en,ru;q=0.9,he;q=0.8",
                "if-modified-since": "Fri, 03 Jan 2025 15:16:30 GMT",
                "priority": "u=1, i",
                "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
                "sec-ch-ua-mobile": "?0",
                "sec-ch-ua-platform": '"macOS"',
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-origin",
                "x-requested-with": "XMLHttpRequest",
            },
            cookies=self.cookies,
        )
        alerts = r.content.decode("UTF-8").replace("\n", "").replace("\r", "")
        if len(alerts) <= 1:
            return None
        # parse the json response
        j = json.loads(r.content)
        return j

    def get_red_alerts(self):
        # get red alerts
        HOST = "https://www.oref.org.il/WarningMessages/alert/alerts.json"
        r = requests.get(HOST, headers=self.headers, cookies=self.cookies)
        alerts = r.content.decode("UTF-8").replace("\n", "").replace("\r", "")
        if len(alerts) <= 1:
            return None
        # parse the json response
        j = json.loads(r.content)
        # check if there is no alerts - if so, return null.
        if len(j["data"]) == 0:
            return None
        # initialize the current timestamp to know when the rocket alert started
        j["timestamp"] = time.time()
        # parse data
        return j
