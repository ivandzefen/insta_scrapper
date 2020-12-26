'''
Instagram scrapper
scraps the names and number of followers of users who have used a particular tag
'''
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import time
#from selenium.webdriver.common.keys import keys
def get
def get_info():
    '''  
    prompts the user name, password, tag and number of instagram users whose info are required 
    ''' 
    usr=str(input('give user name :'))
    psw=str(input('give password :'))
    tag=str(input('give tag to scrap :'))
    while True:
        try :
            number=int(input('how much info do you want(enter 0 for all) '))
            if number<0 :
                print('please enter an integer greater than 0')
                continue
            break
        except :
            print('please enter an integer greater than 0')
            continue
    return (usr,psw,tag,number)
    
def login_insta(driver,usrn,psw):
    '''
    logs in to instagram
    parameters
        driver : selenium driver
        usrn : instagram username
        psw : instagram password
    '''
    try:
        driver.get('https://www.instagram.com')
        time.sleep(1)
        usr=driver.find_element_by_name('username')
        usr.send_keys(usrn)
        del(usr)
        pswd=driver.find_element_by_name('password')
        pswd.send_keys(psw)
        del(pswd)
        login=driver.find_element_by_class_name('L3NKy')
        login.click()
    except e:
        print(e)
    
def scrap_names(driver,hashtag,number):
    '''
    searhs for a # and gets the handle of a number of users who used the #
    parameters
        driver : selenium webdriver
        hashtag : # to be searched
        number : number of users handled to be collected(collects all if 0)
    PS: the driver should be logged into an instagram account
    '''
    names=[]
    i=number if number>0 else -1
    onpic=True
    skipped=0
    consecutiveskipped=0
    try :
        print('trying')
        driver.get('https://www.instagram.com/explore/tags/'+hashtag+'/')
    except e:
        print('failed')
        print(e)
        return names
    try :
        pic=driver.find_element_by_class_name('v1Nh3')
    except :
        return names
    pic.click()
    while onpic and i!=0 and consecutiveskipped<10:
        time.sleep(1)
        try :
            name=driver.find_element_by_class_name('yWX7d')
            consecutiveskipped=0
        except :
            skipped+=1
            consecutiveskipped+=1
            print('skipped:',skipped)
            onpic=next_pic(driver)
            continue    
        name=name.text
        names.append(name)
        i-=1
        print(number-i,':',name)
        onpic=next_pic(driver)
    if consecutiveskipped>=10:
        print("check your connection")
    return names
    
def get_followers(driver,names):
    '''
    gets the number of followers for every handle in a list
    parameters
        driver : selenium webdriver 
        names : list of instagram handles
    PS: the driver should be logged into an instagram account
    '''
    followers=['']*len(names)
    for i in range(len(names)):
        try :
            driver.get('https://www.instagram.com/'+names[i])
        except e:
            print(i)
            continue
        time.sleep(1)
        follower=driver.find_elements_by_class_name('g47SY')
        followers[i]=follower[1].get_attribute('title')
        print(names[i],':',followers[i])
    return followers
    
def next_pic(driver):
    '''
    clicks on the next arrow on an instagram picture
    parameters 
        driver : selenium webdriver
    PS: the driver should be on an instagram picture
    '''
    try :
        next=driver.find_element_by_class_name('coreSpriteRightPaginationArrow')
        next.click()
        return True
    except :
        return False    
        
def start():
    t=time.localtime()
    year=str(t.tm_year)
    mon=str(t.tm_mon)
    day=str(t.tm_mday)
    hour=str(t.tm_hour)
    minute=str(t.tm_min)
    sec=str(t.tm_sec)
    dayTime=year+'-'+mon+'-'+day+'_'+hour+':'+minute+':'+sec
    username,password,hashtag,number=get_info()
    driver=webdriver.Firefox()
    login_insta(driver,username,password)
    time.sleep(10)
    names=scrap_names(driver,hashtag,number)
    followers=get_followers(driver,names)
    with open('scrap_'+dayTime+'.csv','w') as file:
        print('name,followers',file=file)
        for i in range(len(names)):
            print(names[i]+','+followers[i],file=file)
    driver.close()
    
if __name__=='__main__':
    start()
