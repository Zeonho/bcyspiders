import urllib.request 
import socket 
import re 
import threading
import os

socket.setdefaulttimeout(120)

user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
headers = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'Cookie':'lang_set=zh; PHPSESSID=nvsr465e2jg2649qppfg2a8mu6; LOGGED_USER=lTwxSY5lDVJPM%2BT0EbbYG9U%3D%3AG0z5gEbKWifwFBQAllg7Og%3D%3D; CNZZDATA1257708097=1414919653-1467784413-null%7C1470512244; Hm_lvt_330d168f9714e3aa16c5661e62c00232=1470348021; Hm_lpvt_330d168f9714e3aa16c5661e62c00232=1470513179; mobile_set=no',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}



hostname = "http://bcy.net/coser/allcoser"
initword = 'welcome\n \nThis is a program that searches and downloads photo automatically from bcy.net \n\nthe photo will be downloaded on the dictory of this program'

banchar = '\/:*?"<>→'
picfile = os.getcwd() + '\\' + 'picture'
if not os.path.isdir(picfile):
    os.mkdir(picfile)
pathbackup = os.getcwd() + '\\' + 'picture' + '\\' + 'sp'
if not os.path.isdir(pathbackup):
    os.mkdir(pathbackup)



def printinfo(address,title,name):
    try:
        print ('address: ', address)
        print ('title: ',title )
        print ('name: ', name)
    except:
        pass






def getCN(content):
    contentBytes = content
    pattern = "class=.*?blue1.*?>(.*?)</a>"
    #<a href="/u/1053637" class="blue1">AimerLai</a>
    name = list(set(re.findall(pattern, str(contentBytes))))

    return name


def gma():
    if boogetHtml(hostname):
        contentBytes = getHtml(hostname)
        pattern1 = "href=\"/coser/detail[^\"]+\""
        coserweb = list(set(re.findall(pattern1, str(contentBytes))))
        weblist = []
        
        for i in coserweb:
            i = i.strip("\"")
            i = i.replace("href=\"","http://bcy.net")
            weblist.append(i)

        return weblist

    
    """
    text2 = open('namelist.txt','w')
    for j in cosername:

        text2.write(j + '\n')
    text2.close()
    """

def getImg(content):
    contentBytes = content
    pattern1 = "detail_clickable.*?http://img[^\s].bcyimg.com/coser/[\S]+[/w650]"
    pattern2 = "<img.*?class=.*?detail_std.*?detail_clickable.*?src='(.*?)/w650.*?>"
    #<img class="detail_std detail_clickable" src="http://img5.bcyimg.com/coser/63053/post/c046d/04055752e0bb468680d9167be6fa5805.jpg/w650">
    imgList = list(re.findall(pattern2, str(contentBytes)))
    return imgList
        
        
    

def getTitle(content):
    contentBytes = content
    pattern1 = "<h1.*?class=.*?js-post-title.*?>\n(.+)</h1>"
    #<h1 class="js-post-title">【剑网三】慕容追风&amp;卓婉清 </h1>

    name = re.findall(pattern1, str(contentBytes))
    name = str(name)
    for x in banchar:
        name = name.replace(x,'')
    
    if name == '[]':
        return '[no title]'
    return name

def saveImg(link,title,name):
    threads = []
    imgList = getImg(link)
    path = os.getcwd()
    path += '\\' + 'picture' + '\\'
    path += title
    x = 0
    if not os.path.isdir(path):
        try:
            os.mkdir(path)
        except OSError as e:
            print(e,"putting them to sp")
            path = pathbackup

    for image in imgList:
        imgname = path + r'\\'+ name  + str(x)+".jpg"
        task = threading.Thread(target=save,args=(image,imgname))
        threads.append(task)
        x += 1
    for t in threads:
        t.setDaemon(True)
        try:
            t.start()
        except:
            print('fail to save')


def save(imagelink,path):
    try:
        urllib.request.urlretrieve(imagelink,path)
    except urllib.error.HTTPError as e:
        print (e)
    except ConnectionAbortedError:
        print("ConnectionAbortedError")
    except:
        print ("Some error happen, and i don't know what it is -_-")
        


def getHtml(url):
    req = urllib.request.Request(url,headers=headers)
    webpage = urllib.request.urlopen(req)
    contentBytes = webpage.read().decode('utf-8')
    return contentBytes

def boogetHtml(url):
    req = urllib.request.Request(url,headers=headers)
    try:
        webpage = urllib.request.urlopen(req)
    except urllib.error.HTTPError:
        print("HTTPError")
        return False
    except ConnectionAbortedError:
        return False
    except:
        print ("some error appear")
        return False
    else: 
        return True

def run():
    count = 1
    resultcount = len(gma())
    print (initword)
    print ('searching')
    print('found result: ',resultcount)
    print()

    
    for link in gma():
        try:
            content = getHtml(link)
            title = str(getTitle(content))
            namelist = getCN(content)
            name = ""
            if namelist != None and namelist != []:
                for n in namelist:
                    name += str(n).strip("'")

            
            print(int(count/resultcount*100),'%')
            printinfo(link,title,name)

            
            print('downloading...')
            saveImg(content,title,name)
            print('complete')
        except ConnectionAbortedError as e:
            print("ConnectionAbortedError")
        except:
            print('error in saveing')


        
        count += 1
        
        print ()
    print ("\nall done")
    print ("total: ",resultcount)
 
if __name__ == "__main__":
    run()
    


            
  
    


  
       

