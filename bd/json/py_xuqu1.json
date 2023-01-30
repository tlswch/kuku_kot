#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..') 
from base.spider import Spider
import json
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "戏曲专栏"
	def init(self,extend=""):
		print("============{0}============".format(extend))
		pass
	def isVideoFormat(self,url):
		pass
	def manualVideoCheck(self):
		pass
	def homeContent(self,filter):
		result = {}
		cateManual = {
			 "京剧":"京剧超清",
 "越剧":"越剧超清",
 "蒲剧":"蒲剧超清",
 "眉户":"眉户超清",
     "吕剧":"吕剧超清",
     "楚剧":"楚剧超清",
 "歌仔戏":"歌仔戏超清",
    "黄梅戏":"黄梅戏超清",
 "评剧":"评剧超清",
 "豫剧":"豫剧超清",
 "花鼓戏":"花鼓戏超清",    
 "布袋戏":"布袋戏合集超清",    
 "沪剧":"沪剧超清",
 "昆曲":"昆曲超清",
 "潮剧":"潮剧超清",
 "超清潮剧":"超清潮剧超清",
"百花潮剧院":"百花潮剧院超清",
     "香港潮剧":"香港潮剧超清",
     "潮剧院":"潮剧院超清",
    "潮剧团":"潮剧团超清",
     "潮剧全剧":"潮剧全剧超清", 
  "潮剧选段":"潮剧选段超清",
 "名家潮剧":"名家潮剧超清",
   "潮汕小品":"潮汕小品超清",
     "潮汕讲古":"潮汕讲古超清",       
  "绍兴莲花落":"绍兴莲花落超清",
"河北梆子":"河北梆子超清",
 "梆子腔":"梆子腔超清",
 "晋剧":"晋剧超清",
 "龙江剧":"龙江剧超清",
 "越调":"越调超清",
 "河南曲剧":"河南曲剧超清",
 "山东梆子":"山东梆子超清",
 "淮剧":"淮剧超清",
 "滑稽戏":"滑稽戏超清",
 "婺剧":"婺剧超清",
 "绍剧":"绍剧超清",
 "徽剧":"徽剧超清",
 "雁剧":"雁剧超清",
 "上党梆子":"上党梆子超清",
 "秦腔":"秦腔超清",
 "武安平调":"武安平调超清",
 "二人台":"二人台超清",
 "吉剧":"吉剧超清",
 "高腔":"高腔超清"
		}
		classes = []
		for k in cateManual:
			classes.append({
				'type_name':k,
				'type_id':cateManual[k]
			})
		result['class'] = classes
		if(filter):
			result['filters'] = self.config['filter']
		return result
	def homeVideoContent(self):
		result = {
			'list':[]
		}
		return result
	cookies = ''
	def getCookie(self):
		rsp = self.fetch("https://www.bilibili.com/")
		self.cookies = rsp.cookies
		return rsp.cookies
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&duration=4&page={1}'.format(tid,pg)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:			
			rspRetry = self.fetch(url,cookies=self.getCookie())
			content = rspRetry.text		
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">","").replace("</em>","")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id":aid,
				"vod_name":title,
				"vod_pic":img,
				"vod_remarks":remark
			})
		result['list'] = videos
		result['page'] = pg
		result['pagecount'] = 9999
		result['limit'] = 90
		result['total'] = 999999
		return result
	def cleanSpace(self,str):
		return str.replace('\n','').replace('\t','').replace('\r','').replace(' ','')
	def detailContent(self,array):
		aid = array[0]
		url = "https://api.bilibili.com/x/web-interface/view?aid={0}".format(aid)

		rsp = self.fetch(url,headers=self.header)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		title = jo['title'].replace("<em class=\"keyword\">","").replace("</em>","")
		pic = jo['pic']
		desc = jo['desc']
		typeName = jo['tname']
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":"",
			"vod_area":"",
			"vod_remarks":"",
			"vod_actor":"",
			"vod_director":"",
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站'
		vod['vod_play_url'] = playUrl

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		result = {
			'list':[]
		}
		return result
	def playerContent(self,flag,id,vipFlags):
		# https://www.555dianying.cc/vodplay/static/js/playerconfig.js
		result = {}

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid=%20%20{1}&qn=112'.format(ids[0],ids[1])
		rsp = self.fetch(url)
		jRoot = json.loads(rsp.text)
		jo = jRoot['data']
		ja = jo['durl']
		
		maxSize = -1
		position = -1
		for i in range(len(ja)):
			tmpJo = ja[i]
			if maxSize < int(tmpJo['size']):
				maxSize = int(tmpJo['size'])
				position = i

		url = ''
		if len(ja) > 0:
			if position == -1:
				position = 0
			url = ja[position]['url']

		result["parse"] = 0
		result["playUrl"] = ''
		result["url"] = url
		result["header"] = {
			"Referer":"https://www.bilibili.com",
			"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36"
		}
		result["contentType"] = 'video/x-flv'
		return result

	config = {
		"player": {},
		"filter": {}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]