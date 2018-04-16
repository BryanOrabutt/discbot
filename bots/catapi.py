#!/usr/bin/env python3
import requests, re, urlmarker

key = "Mjk4ODU5"

def getCat(imgid=None,category=None):
    str0 = 'http://thecatapi.com/api/images/get?format=html&api_key=' + str(key)
    str1 = ''
    str2 = ''
    if imgid != None:
        str1 = '&image_id=' + str(imgid)
    if category != None:
        str2 = '&category=' + str(category)
    url = str(str0 + str1 + str2)
    resp = requests.get(url)
    data = re.findall(urlmarker.URL_REGEX, str(resp.text))
    img = data[1]
    imgid = re.search(r'(?<=(\?)id=)([\w-]+)', str(data[0]))
    retval = [str(img), str(imgid[0])]
    return retval
   
def getCategories():
    resp = requests.get('http://thecatapi.com/api/categories/list')
    elems = re.findall(r'<name>(.*?)</name>', str(resp.text))
    return elems

def vote(userid,imgid,score):
    str0 = 'http://thecatapi.com/api/images/vote?api_key=' + str(key)
    str1 = '&sub_id=' + str(userid)
    str2 = '&image_id=' + str(imgid)
    str3 = '&scre=' + str(score)
    url = str0 + str1 + str2 + str3
    resp = requests.get(url)
    
def favourite(userid, imgid, addrm):
    str0 = 'http://thecatapi.com/api/images/favourite?api_key=' + str(key)
    str1 = '&sub_id=' + str(userid)
    str2 = '&image_id=' + str(imgid)
    str3 = '&action=' + str(addrm)
    url = str0 + str1 + str2 + str3
    resp = requests.get(url)

def getFavs(userid):
    str0 = 'http://thecatapi.com/api/images/getfavourites?format=xml' 
    str1 = '&api_key=' + str(key)
    str2 = '&sub_id=' + str(userid)
    url = str0 + str1 + str2
    resp = requests.get(url)
    favs = re.findall(r'<url>(.*?)</url>', resp.text)
    return favs

def report(userid, imgid, reason=None):
    str0 = 'http://thecatapi.com/images/report?api_key=' + str(key)
    str1 = '&image_id=' + str(imgid)
    str2 = '&userid=' + str(userid)
    str3 =  ''
    if reason != None:
        str3 = str(reason)
        str3.replace(' ', '%20')
    url = str0 + str1 + str2 + str3
    resp = requests.get(url)

