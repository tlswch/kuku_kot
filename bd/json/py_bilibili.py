#coding=utf-8
#!/usr/bin/python
import sys
sys.path.append('..')
from base.spider import Spider
import json
from requests import session, utils
import os
import time
import base64

class Spider(Spider):  # 元类 默认的元类 type
	def getName(self):
		return "B站视频"
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
		
			"演唱会":"演唱会4K",
      "MV":"MV4K",
      "窗白噪音":"窗白噪音4K",
      "风景":"风景4K",
      "说案":"说案",
      "戏曲":"戏曲4K",
      "演讲":"演讲4K",
      "解说":"解说",
      "相声小品":"相声小品",
      "河卫国风":"河南卫视国风4K",
      "儿童":"儿童",
      "苏教版":"苏教版课程",
      "人教版":"人教版课程",
      "沪教版":"沪教版课程",
      "北师大版":"北师大版课程",
      "球星":"球星",
      "动物世界":"动物世界4K"
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
		cookies_str ="buvid3=418CAE55-A89A-0098-4B2B-C7F6E828462038635infoc; rpdid=|(u)~kmY)kml0J'uYkukRYRRJ; video_page_version=v_old_home_6; buvid_fp=418CAE55-A89A-0098-4B2B-C7F6E828462038635infoc; buvid_fp_plain=6463AA03-B557-A6CF-6E13-6309086EB29041849infoc; i-wanna-go-back=-1; CURRENT_BLACKGAP=0; CURRENT_QUALITY=80; blackside_state=0; nostalgia_conf=-1; fingerprint=63b8c1cbf6ab858bf9a04a9ff112f9bb; SESSDATA=2472ade8,1677739051,a03fc*91; bili_jct=b0d218df4c5be5b7f26d3b0ae390e826; DedeUserID=667298592; DedeUserID__ckMd5=aa18ade6353974c9; sid=5o3z9v5c; bp_video_offset_667298592=undefined; b_ut=5; CURRENT_FNVAL=16; innersign=0" #填入大会员Cookies
		cookies_dic = dict([co.strip().split('=') for co in cookies_str.split(';')])
		rsp = session()
		cookies_jar = utils.cookiejar_from_dict(cookies_dic)
		rsp.cookies = cookies_jar
		self.cookies = rsp.cookies
		return rsp.cookies
	def categoryContent(self,tid,pg,filter,extend):		
		result = {}
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}&page={1}'.format(tid,pg)
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
		timeStamp = jo['pubdate']
		timeArray = time.localtime(timeStamp)
		year = str(time.strftime("%Y-%m-%d %H:%M", timeArray)).replace(" ","/")
		dire = jo['owner']['name']
		typeName = jo['tname']
		remark = str(jo['duration']).strip()
		vod = {
			"vod_id":aid,
			"vod_name":title,
			"vod_pic":pic,
			"type_name":typeName,
			"vod_year":year,
			"vod_area":"",
			"vod_remarks":remark,
			"vod_actor":"",
			"vod_director":dire,
			"vod_content":desc
		}
		ja = jo['pages']
		playUrl = ''
		for tmpJo in ja:
			cid = tmpJo['cid']
			part = tmpJo['part']
			playUrl = playUrl + '{0}${1}_{2}#'.format(part,aid,cid)

		vod['vod_play_from'] = 'B站视频'
		vod['vod_play_url'] = playUrl

		result = {
			'list':[
				vod
			]
		}
		return result
	def searchContent(self,key,quick):
		url = 'https://api.bilibili.com/x/web-interface/search/type?search_type=video&keyword={0}'.format(key)
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
		content = rsp.text
		jo = json.loads(content)
		if jo['code'] != 0:
			rspRetry = self.fetch(url, cookies=self.getCookie())
			content = rspRetry.text
		jo = json.loads(content)
		videos = []
		vodList = jo['data']['result']
		for vod in vodList:
			aid = str(vod['aid']).strip()
			title = vod['title'].strip().replace("<em class=\"keyword\">", "").replace("</em>", "")
			img = 'https:' + vod['pic'].strip()
			remark = str(vod['duration']).strip()
			videos.append({
				"vod_id": aid,
				"vod_name": title,
				"vod_pic": img,
				"vod_remarks": remark
			})
		result = {
			'list': videos
		}
		return result


	def playerContent(self,flag,id,vipFlags):
		result = {}

		ids = id.split("_")
		url = 'https://api.bilibili.com:443/x/player/playurl?avid={0}&cid={1}&qn=116'.format(ids[0],ids[1])
		if len(self.cookies) <= 0:
			self.getCookie()
		rsp = self.fetch(url,cookies=self.cookies)
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
		"filter": {
		"演唱会": [
      {
        "key": "tid",
        "name": "分类",
        "value": [
          {
            "n": "全部",
            "v": "演唱会"
          },
          {
                        "n":"邓丽君",
                        "v":"邓丽君"
                    },
                     {
                        "n":"蔡琴",
                        "v":"蔡琴"
                    }, 
                    {
                        "n":"李娜",
                        "v":"李娜"
                    },
                     {
                        "n":"马玉涛",
                        "v":"马玉涛"
                    },
                     {
                        "n":"李谷一",
                        "v":"李谷一"
                    },
                     {
                        "n":"宋祖英",
                        "v":"宋祖英"
                    },
                     {
                        "n":"殷秀梅",
                        "v":"殷秀梅"
                    },
                    {
                        "n":"郭兰英",
                        "v":"郭兰英"
                    },
                    {
                        "n":"李双江",
                        "v":"李双江"
                    },
                    {
                        "n":"王二妮",
                        "v":"王二妮"
                    },
                    {
                        "n":"刘德华",
                        "v":"刘德华"
                    },
                    {
                        "n":"郭富城",
                        "v":"郭富城"
                    },
                    {
                        "n":"张学友",
                        "v":"张学友"
                    },
                    {
                        "n":"黎明",
                        "v":"黎明"
                    },
                    {
                        "n":"李宗盛",
                        "v":"李宗盛"
                    },
                    {
                        "n":"朴树",
                        "v":"朴树"
                    },
                    {
                        "n":"林子祥",
                        "v":"林子祥"
                    },
                    {
                        "n":"任贤齐",
                        "v":"任贤齐"
                    },
                    {
                        "n":"张信哲",
                        "v":"张信哲"
                    },
                    {
                        "n":"孙楠",
                        "v":"孙楠"
                    },
                    {
                        "n":"张宇",
                        "v":"张宇"
                    },
                    {
                        "n":"周华健",
                        "v":"周华健"
                    },
                    {
                        "n":"蔡依林",
                        "v":"蔡依林"
                    },
                    {
                        "n":"薛之谦",
                        "v":"薛之谦"
                    },
                    {
                        "n":"洛天依",
                        "v":"洛天依"
                    },
                    {
                        "n":"初音未来",
                        "v":"初音未来"
                    },
                    {
                        "n":"许嵩",
                        "v":"许嵩"
                    },
                    {
                        "n":"戴佩妮",
                        "v":"戴佩妮"
                    },
                    {
                        "n":"邓紫棋",
                        "v":"邓紫棋"
                    },
                    {
                        "n":"张韶涵",
                        "v":"张韶涵"
                    },
                    {
                        "n":"蔡健雅",
                        "v":"蔡健雅"
                    },
                    {
                        "n":"莫文蔚",
                        "v":"莫文蔚"
                    },
                    {
                        "n":"刘若英",
                        "v":"刘若英"
                    },
                    {
                        "n":"周深",
                        "v":"周深"
                    },
                    {
                        "n":"毛不易",
                        "v":"毛不易"
                    },
                    {
                        "n":"汪苏泷",
                        "v":"汪苏泷"
                    },
                    {
                        "n":"李宇春",
                        "v":"李宇春"
                    },
                    {
                        "n":"徐佳莹",
                        "v":"徐佳莹"
                    },
                    {
                        "n":"杨宗纬",
                        "v":"杨宗纬"
                    },
                    {
                        "n":"胡彦斌",
                        "v":"胡彦斌"
                    },
                    {
                        "n":"杨千嬅",
                        "v":"杨千嬅"
                    },
                    {
                        "n":"张靓颖",
                        "v":"张靓颖"
                    },
                    {
                        "n":"李荣浩",
                        "v":"李荣浩"
                    },
                    {
                        "n":"杨丞琳",
                        "v":"杨丞琳"
                    },
                    {
                        "n":"林志炫",
                        "v":"林志炫"
                    },
                    {
                        "n":"陶喆",
                        "v":"陶喆"
                    },
                    {
                        "n":"胡夏",
                        "v":"胡夏"
                    },
                    {
                        "n":"李玉刚",
                        "v":"李玉刚"
                    },
                    {
                        "n":"弦子",
                        "v":"弦子"
                    },
                    {
                        "n":"陈小春",
                        "v":"陈小春"
                    },
                    {
                        "n":"萧亚轩",
                        "v":"萧亚轩"
                    },
                    {
                        "n":"鹿晗",
                        "v":"鹿晗"
                    },
                    {
                        "n":"纵贯线",
                        "v":"纵贯线"
                    },
                    {
                        "n":"许巍",
                        "v":"许巍"
                    },
                    {
                        "n":"林俊杰",
                        "v":"林俊杰"
                    },
                    {
                        "n":"赵雷",
                        "v":"赵雷"
                    },
                    {
                        "n":"谭咏麟",
                        "v":"谭咏麟"
                    },
                    {
                        "n":"凤凰传奇",
                        "v":"凤凰传奇"
                    },
                    {
                        "n":"容祖儿",
                        "v":"容祖儿"
                    },
                    {
                        "n":"周传雄",
                        "v":"周传雄"
                    },
                    {
                        "n":"SHE",
                        "v":"SHE"
                    },
                    {
                        "n":"苏打绿",
                        "v":"苏打绿"
                    },
                    {
                        "n":"五月天",
                        "v":"五月天"
                    },
                    {
                        "n":"张国荣",
                        "v":"张国荣"
                    },
                    {
                        "n":"梅艳芳",
                        "v":"梅艳芳"
                    },
                    {
                        "n":"孙燕姿",
                        "v":"孙燕姿"
                    },
                    {
                        "n":"李健",
                        "v":"李健"
                    },
                    {
                        "n":"华晨宇",
                        "v":"华晨宇"
                    },
                    {
                        "n":"袁娅维",
                        "v":"袁娅维"
                    },
                    {
                        "n":"大张伟",
                        "v":"大张伟"
                    },
                    {
                        "n":"TFBOYS",
                        "v":"TFBOYS"
                    },
                    {
                        "n":"王俊凯",
                        "v":"王俊凯"
                    },
                    {
                        "n":"易烊千玺",
                        "v":"易烊千玺"
                    },
                    {
                        "n":"王源",
                        "v":"王源"
                    },
                    {
                        "n":"田馥甄",
                        "v":"田馥甄"
                    },
                    {
                        "n":"小虎队",
                        "v":"小虎队"
                    },
                    {
                        "n":"张杰",
                        "v":"张杰"
                    },
                    {
                        "n":"王菲",
                        "v":"王菲"
                    },
                    {
                        "n":"伍佰",
                        "v":"伍佰"
                    },
                    {
                        "n":"刀郎",
                        "v":"刀郎"
                    },
                    {
                        "n":"草蜢",
                        "v":"草蜢"
                    },
                    {
                        "n":"潘玮柏",
                        "v":"潘玮柏"
                    },
                    {
                        "n":"梁静茹",
                        "v":"梁静茹"
                    },
                    {
                        "n":"林宥嘉",
                        "v":"林宥嘉"
                    },
                    {
                        "n":"蔡徐坤",
                        "v":"蔡徐坤"
                    },
                    {
                        "n":"周慧敏",
                        "v":"周慧敏"
                    },
                    {
                        "n":"李圣杰",
                        "v":"李圣杰"
                    },
                    {
                        "n":"张惠妹",
                        "v":"张惠妹"
                    },
                    {
                        "n":"萧敬腾",
                        "v":"萧敬腾"
                    },
                    {
                        "n":"周笔畅",
                        "v":"周笔畅"
                    },
                    {
                        "n":"焦迈奇",
                        "v":"焦迈奇"
                    },
                    {
                        "n":"尤长靖",
                        "v":"尤长靖"
                    },
                    {
                        "n":"郑中基",
                        "v":"郑中基"
                    },
                    {
                        "n":"谭维维",
                        "v":"谭维维"
                    },
                    {
                        "n":"陈慧娴",
                        "v":"陈慧娴"
                    },
                    {
                        "n":"张艺兴",
                        "v":"张艺兴"
                    },
                    {
                        "n":"王嘉尔",
                        "v":"王嘉尔"
                    },
                    {
                        "n":"刘宪华",
                        "v":"刘宪华"
                    },
                    {
                        "n":"张敬轩",
                        "v":"张敬轩"
                    },
                    {
                        "n":"李克勤",
                        "v":"李克勤"
                    },
                    {
                        "n":"阿杜",
                        "v":"阿杜"
                    },
                    {
                        "n":"郭静",
                        "v":"郭静"
                    },
                    {
                        "n":"崔健",
                        "v":"崔健"
                    },
                    {
                        "n":"庾澄庆",
                        "v":"庾澄庆"
                    },
                    {
                        "n":"汪峰",
                        "v":"汪峰"
                    },
                    {
                        "n":"那英",
                        "v":"那英"
                    },
                    {
                        "n":"杨坤",
                        "v":"杨坤"
                    },
                    {
                        "n":"叶倩文",
                        "v":"叶倩文"
                    },
                    {
                        "n":"王心凌",
                        "v":"王心凌"
                    },
                    {
                        "n":"张震岳",
                        "v":"张震岳"
                    },
                    {
                        "n":"韩红",
                        "v":"韩红"
                    },
                    {
                        "n":"齐秦",
                        "v":"齐秦"
                    },
                    {
                        "n":"张雨生",
                        "v":"张雨生"
                    },
                    {
                        "n":"黄品源",
                        "v":"黄品源"
                    },
                    {
                        "n":"林忆莲",
                        "v":"林忆莲"
                    },
                    {
                        "n":"丁当",
                        "v":"丁当"
                    },
                    {
                        "n":"郑智化",
                        "v":"郑智化"
                    },
                    {
                        "n":"李玟",
                        "v":"李玟"
                    },
                    {
                        "n":"谢霆锋",
                        "v":"谢霆锋"
                    },
                    {
                        "n":"黄小琥",
                        "v":"黄小琥"
                    },
                    {
                        "n":"徐小凤",
                        "v":"徐小凤"
                    },
                    {
                        "n":"任嘉伦",
                        "v":"任嘉伦"
                    },
                    {
                        "n":"卓依婷",
                        "v":"卓依婷"
                    },
                    {
                        "n":"逃跑计划",
                        "v":"逃跑计划"
                    },
                    {
                        "n":"青鸟飞鱼",
                        "v":"青鸟飞鱼"
                    },
                    {
                        "n":"飞儿乐队",
                        "v":"飞儿乐队"
                    },
                    {
                        "n":"花儿乐队",
                        "v":"花儿乐队"
                    },
                    {
                        "n":"南拳妈妈",
                        "v":"南拳妈妈"
                    },
                    {
                        "n":"水木年华",
                        "v":"水木年华"
                    },
                    {
                        "n":"动力火车",
                        "v":"动力火车"
                    },
                    {
                        "n":"筷子兄弟",
                        "v":"筷子兄弟"
                    },
                    {
                        "n":"鹿先森乐队",
                        "v":"鹿先森乐队"
                    },
                    {
                        "n":"信乐队",
                        "v":"信乐队"
                    },
                    {
                        "n":"旅行团乐队",
                        "v":"旅行团乐队"
                    },
                    {
                        "n":"By2",
                        "v":"By2"
                    },
                    {
                        "n":"郁可唯",
                        "v":"郁可唯"
                    },
                    {
                        "n":"宋亚森",
                        "v":"宋亚森"
                    },
                    {
                        "n":"费玉清",
                        "v":"费玉清"
                    },
                    {
                        "n":"费翔",
                        "v":"费翔"
                    },
                    {
                        "n":"金志文",
                        "v":"金志文"
                    },
                    {
                        "n":"黄家强",
                        "v":"黄家强"
                    },
                    {
                        "n":"方大同",
                        "v":"方大同"
                    },
                    {
                        "n":"吴克群",
                        "v":"吴克群"
                    },
                    {
                        "n":"罗大佑",
                        "v":"罗大佑"
                    },
                    {
                        "n":"光良",
                        "v":"光良"
                    },
                    {
                        "n":"田震",
                        "v":"田震"
                    },
                    {
                        "n":"凤飞飞",
                        "v":"凤飞飞"
                    },
                    {
                        "n":"谭晶",
                        "v":"谭晶"
                    },
                    {
                        "n":"王杰",
                        "v":"王杰"
                    },
                    {
                        "n":"羽泉",
                        "v":"羽泉"
                    },
                    {
                        "n":"金池",
                        "v":"金池"
                    },
                    {
                        "n":"屠洪刚",
                        "v":"屠洪刚"
                    },
                    {
                        "n":"戴荃",
                        "v":"戴荃"
                    },
                    {
                        "n":"郭采洁",
                        "v":"郭采洁"
                    },
                    {
                        "n":"罗志祥",
                        "v":"罗志祥"
                    },
                    {
                        "n":"王力宏",
                        "v":"王力宏"
                    },
                    {
                        "n":"林肯公园",
                        "v":"林肯公园"
                    },
                    {
                        "n":"迈克尔杰克逊",
                        "v":"迈克尔杰克逊"
                    },
                    {
                        "n":"泰勒·斯威夫特",
                        "v":"泰勒·斯威夫特"
                    },
                    {
                        "n":"阿黛尔",
                        "v":"阿黛尔"
                    },
                    {
                        "n":"BIGBANG",
                        "v":"BIGBANG"
                    },
                    {
                        "n":"LadyGaga",
                        "v":"LadyGaga"
                    },
                    {
                        "n":"贾斯丁比伯",
                        "v":"贾斯丁比伯"
                    },
                    {
                        "n":"中岛美雪",
                        "v":"中岛美雪"
                    },
                    {
                        "n":"仓木麻衣",
                        "v":"仓木麻衣"
                    },
                    {
                        "n":"后街男孩",
                        "v":"后街男孩"
                    },
                    {
                        "n":"布兰妮",
                        "v":"布兰妮"
                    },
                    {
                        "n":"夜愿乐队",
                        "v":"夜愿乐队"
                    }
        ]
      },
	        {
        "key": "duration",
        "name": "时长",
        "value": [
          {
            "n": "全部",
            "v": "0"
          },
          {
            "n": "60分钟以上",
            "v": "4"
          },
          {
            "n": "30~60分钟",
            "v": "3"
          },
          {
            "n": "10~30分钟",
            "v": "2"
          },
          {
            "n": "10分钟以下",
            "v": "1"
          }
        ]
      }
    ]}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]	

	config = {
		"player": {},
		"filter": {
		"相声小品": [
      {
        "key": "tid",
        "name": "分类",
        "value": [
          {
            "n": "全部",
            "v": "相声小品"
          },
          {
            "n": "单口相声",
            "v": "单口相声"
          },
          {
            "n": "群口相声",
            "v": "群口相声"
          },
          {
            "n": "德云社",
            "v": "德云社"
          },
          {
            "n": "青曲社",
            "v": "青曲社"
          },
          {
            "n": "郭德纲",
            "v": "郭德纲"
          },
          {
            "n": "岳云鹏",
            "v": "岳云鹏"
          },
          {
            "n": "曹云金",
            "v": "曹云金"
          },
          {
            "n": "评书",
            "v": "评书"
          },
          {
            "n": "小曲",
            "v": "小曲"
          },
          {
            "n": "二人转",
            "v": "二人转"
          },
          {
            "n": "春晚小品",
            "v": "春晚小品"
          },
          {
            "n": "赵本山",
            "v": "赵本山"
          },
          {
            "n": "陈佩斯",
            "v": "陈佩斯"
          },
          {
            "n": "冯巩",
            "v": "冯巩"
          },
          {
            "n": "宋小宝",
            "v": "宋小宝"
          },
          {
            "n": "赵丽蓉",
            "v": "赵丽蓉"
          },
          {
            "n": "郭达",
            "v": "郭达"
          },
          {
            "n": "潘长江",
            "v": "潘长江"
          },
          {
            "n": "郭冬临",
            "v": "郭冬临"
          },
          {
            "n": "严顺开",
            "v": "严顺开"
          },
          {
            "n": "文松",
            "v": "文松"
          },
          {
            "n": "开心麻花",
            "v": "开心麻花"
          },
          {
            "n": "屌丝男士",
            "v": "屌丝男士"
          },
          {
            "n": "喜剧综艺",
            "v": "喜剧综艺"
          }
        ]
      },
	        {
        "key": "duration",
        "name": "时长",
        "value": [
          {
            "n": "全部",
            "v": "0"
          },
          {
            "n": "60分钟以上",
            "v": "4"
          },
          {
            "n": "30~60分钟",
            "v": "3"
          },
          {
            "n": "10~30分钟",
            "v": "2"
          },
          {
            "n": "10分钟以下",
            "v": "1"
          }
        ]
      }
    ]}
	}
	header = {}

	def localProxy(self,param):
		return [200, "video/MP2T", action, ""]