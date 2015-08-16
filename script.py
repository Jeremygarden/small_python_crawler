import time
import sys
import urllib
import urllib2
import cookielib
import os
import re
from bs4 import BeautifulSoup
 
class renrenSpider:    
 
    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.domain = 'renren.com'
        self.id = ''
        self.sid = ''
        try:
            self.cookie = cookielib.CookieJar()
            self.cookieProc = urllib2.HTTPCookieProcessor(self.cookie)
        except:
            raise
        else:
            opener = urllib2.build_opener(self.cookieProc)
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11')]
            urllib2.install_opener(opener)
     
    def login(self):
        url='http://3g.renren.com/login.do' 
        postdata = {
                    'email':self.email,
                    'password':self.password,
                    }
         
        req = urllib2.Request(url,urllib.urlencode(postdata))
        index = urllib2.urlopen(req).read()
        indexSoup = BeautifulSoup(index)  
                     
        indexFile = open('index.html','w')
        indexFile.write(indexSoup.prettify())
        indexFile.close()
 
    def getStatus(self):
        #fetching home page
 
        statusDate = [] 
        statusContent = [] 
        originStatusContent = [] 
        url = 'http://3g.renren.com/profile.do' 
        profileGetData = {
                          'id':str(self.id),
                          'sid':self.sid  
                         }
        req = urllib2.Request(url,urllib.urlencode(profileGetData))
        profile = urllib2.urlopen(req).read()
        profileSoup = BeautifulSoup(profile)


        url = profileSoup.select('.sec')[5].find_all('a')[3]['href'] 
        req = urllib2.Request(url)
        statusFile = urllib2.urlopen(req).read()
        statusSoup = BeautifulSoup(statusFile)
        statusFile = open("status.html",'w')
        statusFile.write( statusSoup.prettify())
        statusFile.close()
         
        totalPageHtml = statusSoup.select(".gray")[0].contents
        totalPage = re.findall(r"(?<=/)\d+(?=[^\d])",str(totalPageHtml))
        totalPage = int(totalPage[0])
        print "Total:"+str(totalPage)+"Page"
         
        nowPage = 1
        #set the vale to totalPage = 15
        while (nowPage<=totalPage) :
            print "Currently crawling"+str(nowPage)+"page infomation"
            statusList = statusSoup.select(".list")[0].children
            for child in statusList:

                if (child.select(".time")):#  timestamp
                    statusDate.append(child.select(".time")[0].string) 
                    if (child.select(".forward")): 
                        tempStr = str(child.a.next_element)

                        #forwarding content
                        m = re.findall(r"^.*?(?=Forward)",tempStr)                      
                        if m: 
                            statusContent.append(m[0])
                        else :
                            statusContent.append("Nothing")
 
                        originStatusContent.append(child.select(".forward")[0].a.next_element.next_element) 
                    else:   #original content
                       statusContent.append(child.a.next_element)
                       originStatusContent.append("Nothing")                    
            nowPage = nowPage+1
            if (nowPage>totalPage): break
            req = urllib2.Request(nextPageUrl)
            statusFile = urllib2.urlopen(req).read() 
            statusSoup = BeautifulSoup(statusFile)                            
           # for state in statusList:
           #     print state.name     
         
        finalFile = open("UserData/"+self.id,"w")
        for i in range (0,len(statusDate)):
            finalFile.write("The"+str(i+1)+":"+"\n")
            finalFile.write("Time:"+str(statusDate[i])+"\n")
            finalFile.write("Status："+str(statusContent[i])+"\n")
            finalFile.write("Forward："+str(originStatusContent[i])+"\n")
            finalFile.write("\n") 
 
if __name__ == '__main__':
    email = raw_input("Enter your email")
    password = raw_input("Enter your password")
    reload(sys)
    sys.setdefaultencoding('utf-8')  
    renrenLogin = renrenSpider(email,password)
    renrenLogin.login()
    renrenLogin.getStatus() 