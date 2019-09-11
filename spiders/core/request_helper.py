#!/usr/bin/python
#coding=utf-8

import urllib  
import urllib2
import json
import sys,socket,random,time,re
import traceback,logging
import spider_resource
from utils import printInfo,getTime,saveFile
# type = sys.getfilesystemencoding()

def log(err,data):
  printInfo(err,data)
  logger = logging.getLogger()
  logging.LoggerAdapter(logger, None).log(logging.ERROR, err)
  logging.LoggerAdapter(logger, None).log(logging.ERROR, data)

def requestPost(url, data, headers, useIp=False, ssp=None,timeout=15):
  response = None
  if headers: header = headers
  else: header = {}
  if(not header.get('User-Agent')):
    header['User-Agent']=random.choice(spider_resource.useragent)

  try:
    request = { 'header':header, 'url':url, 'proxy':None, 'data':data }
    if(ssp):
      request = ssp.beforeRequest(request)
      header = request['header']
      url = request['url']
      data = request['data']
    if(useIp and request['proxy']): opener = _setProxy(request['proxy'])
    else: opener = urllib2.build_opener()

    req = urllib2.Request(url, data, header)
    response = opener.open(req,None,timeout)
    if(ssp):
      return ssp.afterResponse(response,url)
    return getResponseStr(response.read(),url)
  except Exception as err:
    log(err,url)
  finally:
    if response:
      response.close()

def getResponseStr(htmSource,url):
  html=None
  if(htmSource):
    try:
      html=htmSource.decode("utf-8")
    except:
      try:
        html=htmSource.decode("gb18030")
      except Exception as err:
        log(err,url)
  return html
def setProxyGloab(proxy):
  proxy_handler = urllib2.ProxyHandler({proxy['p']:proxy['ip']})
  opener = urllib2.build_opener(proxy_handler)  
  urllib2.install_opener(opener)  
def _setProxy(proxy):
  print 'proxyip',proxy
  proxy_handler = urllib2.ProxyHandler({proxy['p']:proxy['ip']})
  opener = urllib2.build_opener(proxy_handler)  
  return opener
def dic2tuple(dic):
  tp=[]
  for key in dic:
    tp.append((key,dic[key]))
  return tp

def requestGet(url, headers, useIp, ssp=None,timeout=10):
  if headers: header = headers 
  else: header = {}

  if(not header.get('User-Agent')): header['User-Agent'] = random.choice(spider_resource.useragent)
  request = { 'header':header, 'url':url, 'proxy':None }
  if(ssp): request = ssp.beforeRequest(request)
  header = request['header']
  url = request['url']
  try:
    if(useIp and request['proxy']): opener = _setProxy(request['proxy'])
    else: opener = urllib2.build_opener()
    opener.addheaders = dic2tuple(header)
    response = opener.open(url,None,timeout)
    if(ssp): data = ssp.afterResponse(response,url)
    else: data = getResponseStr(response.read(),url)
    return data
  except Exception as err:
    log(err,url)
  finally:
    if response: response.close()

def extractHtml(url,html,model,modelName,title=None):
  headers = { "Content-Type": "application/json" }
  data={
    'url':url,
    'title':title,
    'html':html,
    'modelName':json.dumps(modelName),
    'model':json.dumps(model),
    'key':"yiyedata_test" 
  }
  data = json.dumps(data)
  # saveFile('extractHtml.txt',data)
  obj = requestPost('http://www.yiyedata.com/api/extracts',data,headers)
  return obj#.decode("UTF-8").encode(type)

def test():
  print 'start'
  user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'# 将user_agent写入头信息 
  headers = { 'User-Agent' : user_agent, "Content-Type": "application/json",#"Content-Length":len(data), 
    "Referer":"http://47.92.87.212:8080/yiye.mgt/view/login.jsp"
  } 
  obj={
    'url':'http://health.sina.com.cn/',
    'title':'北京冬奥会世界新闻机构会议在京举办',
    'html':"",  
    'modelName':'["auto_obj","auto_url"]',
    'model':'[{"Type":3},{"Type":2,"UrlDomains": "all_domain"}]',
    'key':"yiyedata_test" 
  }
  data = json.dumps(obj)
  # data = urllib.urlencode(values)  
  print requestPost('http://www.yiyedata.com/api/extracts',data,headers,None)
# test()
# model=['{"Type":2}','{"Type":3}']
# print json.dumps(model)

# print requestGet('http://health.sina.com.cn/d/2015-05-25/0931171699.shtml',None,None)
