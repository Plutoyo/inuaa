from selenium import webdriver
import requests
import time
import json
import os
import sys
path = os.path.dirname(sys.argv[0])
# url是登录获得cookie的url
url = "https://m.nuaa.edu.cn/uc/wap/login?redirect=https%3A%2F%2Fm.nuaa.edu.cn%2Fncov%2Fwap%2Fdefault%2Findex"
# url2是发送数据的url
url2 = "https://m.nuaa.edu.cn/ncov/wap/default/save"
# serverjam是用来推送微信消息的url,个人使用需要绑定一下自己的微信,这个是绑定的我的微信
serverjam = "https://sc.ftqq.com/SCU114972T4c6e36e5d22020fa744018b929d04ffb5f6a9176526f4.send"
data = {
    "sfzhux": "0",
    "zhuxdz": "",
    "szgj": "",
    "szcs": "",
    "szgjcs": "",
    " sfjwfh": "0",
    "sfyjsjwfh": "0",
    "sfjcjwfh": "0",
    "sflznjcjwfh": "0",
    "sflqjkm": "0",
    "jkmys": "0",
    "sfjtgfxdq": "0",
    "tw": "2",
    "sfcxtz": "0",
    "sfjcbh": "0",
    "sfcxzysx": "0",
    "qksm": "",
    "sfyyjc": "0",
    "jcjgqr": "0",
    "remark": "",
    "address": "江苏省南京市江宁区秣陵街道南京航空航天大学将军路校区慧园学生公寓5号楼",
    "geo_api_info": '''{"type": "complete", "info": "SUCCESS", "status": 1, "XDa": "jsonp_387848_",
                   "position": {"Q": 31.94225, "R": 118.79062999999996, "lng": 118.79063, "lat": 31.94225},
                   "message": "Get ipLocation success.Get address success.", "location_type": "ip", "accuracy": null,
                   "isConverted": true, "addressComponent": {"citycode": "025", "adcode": "320115", "businessAreas": [
            {"name": "开发区", "id": "320115",
             "location": {"Q": 31.925973, "R": 118.80980399999999, "lng": 118.809804, "lat": 31.925973}}],
                                                             "neighborhoodType": "", "neighborhood": "", "building": "",
                                                             "buildingType": "", "street": "胜太路", "streetNumber": "71号",
                                                             "country": "中国", "province": "江苏省", "city": "南京市",
                                                             "district": "江宁区", "township": "秣陵街道"},
                   "formattedAddress": "江苏省南京市江宁区秣陵街道南京航空航天大学将军路校区慧园学生公寓5号楼", "roads": [], "crosses": [], "pois": []}''',
    "area": "江苏省 南京市 江宁区",
    "province": "江苏省",
    "city": "南京市",
    "sfzx": "0",
    "sfjcwhry": "0",
    "sfjchbry": "0",
    "sfcyglq": "0",
    "gllx": "",
    "glksrq": "",
    "jcbhlx": "",
    "jcbhrq": "",
    "ismoved": "0",
    "bztcyy": "",
    "sftjhb": "0",
    "sftjwh": "0",
    "sftjwz": "0",
    "sfjcwzry": "0",
    "jcjg": ""
}


# 时间戳" Hm_lvt_48b682d4885d22a90111e46b972e3268=1600774835; Hm_lpvt_48b682d4885d22a90111e46b972e3268=1600785537"
class iNuaa():
    def __init__(self, id, pwd, push):
        self.id = id
        self.pwd = pwd
        self.push = push
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
            'Cookie': 'eai-sess=%s; UUkey=85868a72a5f464b39cc95b6a04037301;',
            'Host': 'm.nuaa.edu.cn',
            'Origin': 'https://m.nuaa.edu.cn',
            'Referer': 'https://m.nuaa.edu.cn/ncov/wap/default/index',
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin'
        }

    def connect(self):
        Chrome_options = webdriver.ChromeOptions()
        Chrome_options.add_argument('--no-sandbox')
        Chrome_options.add_argument('--disable-dev-shm-usage')
        Chrome_options.add_argument('--headless')
        Chrome_options.add_argument('--disable-gpu')
        web = webdriver.Chrome(options=Chrome_options)
        # web 可视化
        # web = webdriver.Chrome()
        web.get(url)
        time.sleep(3)
        web.find_element_by_xpath('''//div[@class="content"]/div[1]/input''').send_keys(self.id)
        web.find_element_by_xpath('''//div[@class="content"]/div[2]/input''').send_keys(self.pwd)
        web.find_element_by_xpath('''//div[@class="btn"]''').click()
        cookie = {}
        for i in web.get_cookies():
            cookie[i["name"]] = i["value"]
        self.headers['Cookie'] = self.headers['Cookie'] % cookie['eai-sess']
        # 第一次申请需要验证cookies,第二次再发送
        requests.post(url=url2, data=data, headers=self.headers)
        response = requests.post(url=url2, data=data, headers=self.headers)
        try:
            res = json.loads(response.text)
            if res["m"] == "操作成功" and self.push == 1:
                requests.post(serverjam, data={"text": "%d打卡成功" % self.id})
                # print("success")
        except:
            requests.post(serverjam, data={"text": "%d打卡失败" % self.id})
            # print("error")


if __name__ == "__main__":
    usrs = []
    with open(path+"/data.txt", 'r') as f:
        lines = f.readlines()
    for line in lines:
        line = line.strip()
        info = line.split()
        usr_id = int(info[0])
        usr_pwd = info[1]
        usr = iNuaa(usr_id, usr_pwd, int(info[2]))
        usr.connect()
        usrs.append(usr)
