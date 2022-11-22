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
		return "苏联时代"
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
			 "苏联时代":"苏联时代",
"俄罗斯民歌":"俄罗斯民歌",			
"苏联音乐":"苏联音乐",
"苏联歌曲":"苏联歌曲",
"苏联电影":"苏联电影",
"莫斯科大剧院":"莫斯科大剧院",
"莫斯科小剧院":"莫斯科小剧院",
"克里姆林宫剧院":"克里姆林宫剧院",
"马林斯基剧院":"马林斯基剧院",
"基洛夫剧院":"基洛夫剧院",
"俄罗斯国家芭蕾舞剧院":"俄罗斯国家芭蕾舞剧院",
"圣彼得堡芭蕾舞剧院":"圣彼得堡芭蕾舞剧院",
"艾尔米塔什剧院":"艾尔米塔什剧院",
"瓦赫坦戈夫剧院":"瓦赫坦戈夫剧院",
"红旗歌舞团":"红旗歌舞团",
"奥西波夫乐团":"奥西波夫乐团",
"圣彼得堡爱乐乐团":"圣彼得堡爱乐乐团",
"俄罗斯国家爱乐乐团":"俄罗斯国家爱乐乐团",
"苏联电视剧":"苏联电视剧",
"战斗民族":"战斗民族",
"苏俄轶事":"苏俄轶事",
"苏联文艺":"苏联文艺",
"苏联文化":"苏联文化",
"苏联文学":"苏联文学",
"苏联历史":"苏联历史",
"苏联体育":"苏联体育",
"苏联绘画":"苏联绘画",
"苏联漫画":"苏联漫画",
"苏联宣传画":"苏联宣传画",
"苏联笑话":"苏联笑话",
"苏联动画":"苏联动画",
"苏联美食":"苏联美食",
"苏军":"苏军",
"列宁":"列宁",
"斯大林":"斯大林",
"赫鲁晓夫":"赫鲁晓夫",
"勃列日涅夫":"勃列日涅夫",
"安德罗波夫":"安德罗波夫",
"戈尔巴乔夫":"戈尔巴乔夫",
"叶利钦":"叶利钦",
"普京":"普京",
"梅德韦杰夫":"梅德韦杰夫",
"朱可夫":"科涅夫",
"柴可夫斯基":"柴可夫斯基",
"格林卡":"格林卡",
"里姆斯基·科萨科夫":"里姆斯基·科萨科夫",
"克格勃":"克格勃",
"彼得大帝":"彼得大帝",
"叶卡捷琳娜":"叶卡捷琳娜",
"尼古拉二世":"尼古拉二世",
"十月革命":"十月革命",
"苏联共产党":"苏联共产党"
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