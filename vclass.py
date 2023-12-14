from typing import Optional
import requests as r
from bs4 import BeautifulSoup
from models.Course import Course
from datetime import datetime
import re
import time
import datetime
import sys

class vclass:
    def __init__(self, email:str, password:str):
        self.email = email
        self.password = password
        self.session = r.Session()
        if self._authenticate() == False:
            raise ValueError("Login Error! Make Sure email and Password are valid")
        else:
            print("Success ")

    
    def _doLogin(self):
        res = self.session.get("https://v-class.gunadarma.ac.id/login/index.php")
        cookie = res.cookies.get_dict()
        pattern = '<input type="hidden" name="logintoken" value="\w{32}">'
        token = re.findall(pattern, res.text)[0]
        token = re.findall('\w{32}', token)[0]
        payload = {'username': self.email, 'password': self.password, 'anchor': '', 'logintoken': token}
        response = self.session.post("https://v-class.gunadarma.ac.id/login/index.php", cookies=cookie, data=payload)

        self.cookie = response.cookies.get_dict()
        if 'You are logged in as' in response.text:
            return True
        else :
            return False
    
    def _checkAuth(self):
        checkReq = self.session.get("https://v-class.gunadarma.ac.id/my")
        if 'You are logged in as' in checkReq.text:
            return True
        else :
            return False
        
    def _authenticate(self):
        if self._checkAuth() != True:
            return self._doLogin()
        else :
            return self._checkAuth()
    
    def getAssignmentToday(self):
        response = self.session.get("https://v-class.gunadarma.ac.id/calendar/view.php?view=day")
        data = []
        sp = BeautifulSoup(response.content, 'html.parser')
        allEvent = sp.find('div',class_='eventlist my-1').find_all('div',class_="event m-t-1")
        if allEvent == None:
            return data
        # print(allEvent)
        for event in allEvent:
            descriptionList = event.find('div',class_="description card-body").find_all('div',class_='row')
            dataTemp = {}
            dataTemp['title'] = event['data-event-title']
            dataTemp['course-id'] = event['data-course-id']
            dataTemp['event-id'] = event['data-event-id']
            dataTemp['data'] = []
            x = 0
            for description in descriptionList:
                desc = {}
                getDesc = description.find_all('div')
                desc['title'] = getDesc[0].contents[0]['title']
                desc['text'] = getDesc[1].text
                if getDesc[1].find('a',href=True) != None:
                    desc['link'] = getDesc[1].find('a',href=True)['href']
                else :
                    desc['link'] = ""
                x+=1
                print(desc)
                dataTemp['data'].append(desc)
            data.append(dataTemp)
        print(data)
        return data
    
    def getAssignmentByTimeStamp(self,timestamp:str)-> list['Course']:
        response = self.session.get(f"https://v-class.gunadarma.ac.id/calendar/view.php?view=day&time={timestamp}")
        data: list['Course'] = []
        sp = BeautifulSoup(response.content, 'html.parser')
        allEvent = sp.find('div',class_='eventlist my-1').find_all('div',class_="event m-t-1")
        if allEvent == None:
            return data
        # print(allEvent)
        for event in allEvent:
            descriptionList = event.find('div',class_="description card-body").find_all('div',class_='row')
            dataTemp = {}
            dataTemp['title'] = event['data-event-title']
            dataTemp['course-id'] = event['data-course-id']
            dataTemp['event-id'] = event['data-event-id']
            dataTemp['data'] = []
            x = 0
            for description in descriptionList:
                desc = {}
                getDesc = description.find_all('div')
                desc['title'] = getDesc[0].contents[0]['title']
                desc['text'] = getDesc[1].text
                if getDesc[1].find('a',href=True) != None:
                    desc['link'] = getDesc[1].find('a',href=True)['href']
                else :
                    desc['link'] = ""
                x+=1
                dataTemp['data'].append(desc)
            data.append(Course(dataTemp))
        return data
    
    def getAssignmentByDate(self,date:str=None):
        """Return an Assignemnt by Selected Date with Format : d/m/Y
        """
        if date == None:
            return self.getAssignmentToday()
        else:
            timestamp = time.mktime(datetime.datetime.strptime(date, "%d/%m/%Y").timetuple())
            return self.getAssignmentByTimeStamp(timestamp)
        
    def doLogout(self):
        logout = self.session.get("https://v-class.gunadarma.ac.id/my")
        sp = BeautifulSoup(logout.content,'html.parser')
        logoutLink = sp.find("a",string='Log out',href=True)['href']

        response = self.session.get(logoutLink)

        # print(response.text)
        if "You are not logged in." in response.text:
            return "Successfully logged out"
        else :
            return "Failed To Logout"