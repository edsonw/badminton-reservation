
import utils, json, time

def query(aid, cookie, session_key, bes_time, service_id, sku_id):
    time_list = []
    now = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/api.jsp?cmd=bespeak/initData"
    url += "&aid=%s&yid=1&sessionKey=%s" % (aid, session_key)
    url += "&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&yk_scene=&_page=reserve/add&__from=wxapp" % now
    
    end_time = bes_time + 3600000 * 48 - 1 # 172,799,999
    data = f"aid={aid}&yid=1&storeId=1&serviceId={service_id}&skuId={sku_id}&startTime={bes_time}&endTime={end_time}"
    data += f"&_track=[\"home\/home\",\"serviceDetail\/serviceDetail\",\"reserve\/add\"]&_t={now}&_grp=a&__from=wxapp"
    res = utils.send_request(url, cookie, data)
    
    json_data = json.loads(res.text)
    success = json_data["success"]
    if not success:
        print("query: " + res.text)
        return time_list
    
    for timestamp, info_list in json_data['data'].items():
        for info in info_list:
            if info['num'] < 12:
                time_list.append(timestamp)
                print("    time: %s, reserved: %s" % (utils.transform_millisecond_to_time(timestamp), info['num']))
    
    return time_list

def query_badminton(aid, cookie, session_key, bes_time):
    return query(aid, cookie, session_key, bes_time, 70, 80)

def query_tabletennis(aid, cookie, session_key, bes_time):
    return query(aid, cookie, session_key, bes_time, 72, 84)

def reserve_one_time(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num):
    now = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/api.jsp?cmd=bespeak/add"
    url += "&aid=%s&yid=1&sessionKey=%s" % (aid, session_key)
    url += "&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&fromMid=0" % now
    url += "&mgClueReportInfo={\"sourceModule\":70009,\"sourcePath\":0,\"sourceContentType\":0,\"sourceChannel\":-100,\"sourceType\":2}&yk_scene=&_page=reserve/comfirmRecord&__from=wxapp"
    
    data = "aid=%s&yid=1&note&nextDay=false&besTime=%s&endTime=%s" % (aid, bes_time, end_time)
    data += f"&logicList=%5B%5D&storeId=1&serviceId={service_id}&bespeakNum={num}&mgClueReportInfo=%7B%22sourceModule%22%3A70009%2C%22sourcePath%22%3A0%2C%22sourceContentType%22%3A0%2C%22sourceChannel%22%3A-100%2C%22sourceType%22%3A2%7D"
    data += f"&fromMid=0&name=%E9%99%88%E5%85%88%E7%94%9F&phone=18180890476&bespeakCustomFields=%7B%7D&skuId={sku_id}&channelId=0&formId=1&itemData=%5B%7B%22itemId%22%3A%2263302%22%2C%22itemValue%22%3A%22%22%7D%5D"
    data += "&crossBesTimeList=[{\"besTime\":%s,\"endTime\":%s,\"timeName\":\"\",\"logicList\":[]}]" % (bes_time, end_time)
    data += f"&isUseMemberDiscount=true&itemList=%5B%7B%22type%22%3A1%2C%22price%22%3A0%2C%22subtotal%22%3A0%2C%22num%22%3A{num}%2C%22data%22%3A%7B%22isUseMemberDiscount%22%3Atrue%2C%22serviceId%22%3A{service_id}%2C%22priceType%22%3A0%2C%22skuId%22%3A{sku_id}%2C%22goodsFlag%22%3A1628447953%2C%22goodsPhoto%22%3A%22http%3A%2F%2F28268434.s143i.faiykusr.com%2F2%2F1%2FAI8BCJKvvQ0QAhgAIIDi4p8GKNqDiKkFMIAgOIAg.jpg%22%2C%22memberDiscount%22%3A0%2C%22memberPriceData%22%3A%7B%7D%7D%7D%5D&deductionList=%5B%5D&totalPrice=0&shouldPrice=0&realPrice=0&payType=4&bespeakPay=1&_track=%5B%22home%2Fhome%22%2C%22serviceDetail%2FserviceDetail%22%2C%22reserve%2Fadd%22%2C%22reserve%2FcomfirmRecord%22%5D"
    data += "&_t=%s&_grp=a&__from=wxapp" % now
    
    res = utils.send_request(url, cookie, data)

    print(res.text)
    json_data = json.loads(res.text)
    if "success" in json_data:
        success = json_data["success"]
        if success:
            print("reserve success")
        else:
            print("reserve failed")
    
    return res

def reserve_two_time(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num):
    now = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/api.jsp?cmd=bespeak/add"
    url += "&aid=%s&yid=1&sessionKey=%s" % (aid, session_key)
    url += "&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&fromMid=0" % now
    url += "&mgClueReportInfo={\"sourceModule\":70009,\"sourcePath\":0,\"sourceContentType\":0,\"sourceChannel\":-100,\"sourceType\":2}&yk_scene=&_page=reserve/comfirmRecord&__from=wxapp"
    
    mid_time = bes_time + 3600000
    data = "aid=%s&yid=1&note&nextDay=false&besTime=%s&endTime=%s" % (aid, bes_time, mid_time)
    data += f"&logicList=%5B%5D&storeId=1&serviceId={service_id}&bespeakNum={num}&mgClueReportInfo=%7B%22sourceModule%22%3A70009%2C%22sourcePath%22%3A0%2C%22sourceContentType%22%3A0%2C%22sourceChannel%22%3A-100%2C%22sourceType%22%3A2%7D"
    data += f"&fromMid=0&name=%E9%99%88%E5%85%88%E7%94%9F&phone=18180890476&bespeakCustomFields=%7B%7D&skuId={sku_id}&channelId=0&formId=1&itemData=%5B%7B%22itemId%22%3A%2263302%22%2C%22itemValue%22%3A%22%22%7D%5D"
    data += f"&crossBesTimeList=%5B%7B%22besTime%22%3A{bes_time}%2C%22endTime%22%3A{mid_time}%2C%22timeName%22%3A%22%22%2C%22logicList%22%3A%5B%5D%7D%2C%7B%22besTime%22%3A{mid_time}%2C%22endTime%22%3A{end_time}%2C%22timeName%22%3A%22%22%2C%22logicList%22%3A%5B%5D%7D%5D"
    data += f"&isUseMemberDiscount=true&itemList=%5B%7B%22type%22%3A1%2C%22price%22%3A0%2C%22subtotal%22%3A0%2C%22num%22%3A{num}%2C%22data%22%3A%7B%22isUseMemberDiscount%22%3Atrue%2C%22serviceId%22%3A{service_id}%2C%22priceType%22%3A0%2C%22skuId%22%3A{sku_id}%2C%22goodsFlag%22%3A1628447953%2C%22goodsPhoto%22%3A%22http%3A%2F%2F28268434.s143i.faiykusr.com%2F2%2F1%2FAI8BCJKvvQ0QAhgAIIDi4p8GKNqDiKkFMIAgOIAg.jpg%22%2C%22memberDiscount%22%3A0%2C%22memberPriceData%22%3A%7B%7D%7D%7D%5D&deductionList=%5B%5D&totalPrice=0&shouldPrice=0&realPrice=0&payType=4&bespeakPay=1&_track=%5B%22home%2Fhome%22%2C%22serviceDetail%2FserviceDetail%22%2C%22reserve%2Fadd%22%2C%22reserve%2FcomfirmRecord%22%5D"
    data += "&_t=%s&_grp=a&__from=wxapp" % now
    
    res = utils.send_request(url, cookie, data)

    print(res.text)
    json_data = json.loads(res.text)
    if "success" in json_data:
        success = json_data["success"]
        if success:
            print("reserve success")
        else:
            print("reserve failed")
    
    return res

def reserve_badminton(aid, cookie, session_key, bes_time, end_time, num = 1):
    count = int((end_time - bes_time ) / 3600000)
    if count == 1:
        return reserve_one_time(aid, cookie, session_key, bes_time, end_time, 14, 73, num)
    elif count == 2:
        return reserve_two_time(aid, cookie, session_key, bes_time, end_time, 14, 73, num)

def reserve_tabletennis(aid, cookie, session_key, bes_time, end_time, num = 1):
    count = int((end_time - bes_time ) / 3600000)
    if count == 1:
        return reserve_one_time(aid, cookie, session_key, bes_time, end_time, 72, 84, num)
    elif count == 2:
        return reserve_two_time(aid, cookie, session_key, bes_time, end_time, 72, 84, num)

"""
POST https://m.yk.fkw.com/ajax/myueke_h.jsp?cmd=getSessionKey&aid=28268434&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=1695002161824&wx_scene=1257&yk_scene=&_page=init&__from=wxapp HTTP/1.1
Host: m.yk.fkw.com
Connection: keep-alive
Content-Length: 144
xweb_xhr: 1
cookie: _cliid=Hd6Qx3eksd2p7Pdq; undefined=undefined; _faiHeDistictId=62a979690a8b6cde; _faiHeSessionId=62a9796972898187; _faiHeSesPvStep=1; behaviorData=%7B%22cookieVisitIdMap%22%3A%22%7B70021%3A%5C%22a5e5ace9a7492966%5C%22%7D%22%2C%22cookieNowVisitId%22%3A%22a5e5ace9a7492966%22%7D
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8391
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Accept: */*
Sec-Fetch-Site: cross-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://servicewechat.com/wxa5a9cfd49709ae9e/45/page-frame.html
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh

code=0d33y8000ZYUHQ1k7n100fF6sY33y80S&aid=28268434&yid=1&appid=&appType=1&storeId=1&_track=%5B%22init%22%5D&_t=1695002161822&_grp=a&__from=wxapp
"""

#https://m.yk.fkw.com/ajax/myueke_h.jsp?cmd=getSessionKey&aid=28268434&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=1693969715244&wx_scene=1257&yk_scene=&_page=&__from=wxapp
def get_session_key(aid):
    time = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/myueke_h.jsp?cmd=getSessionKey"
    url += "&aid=%s&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&yk_scene=&_page=&__from=wxapp" % (aid, time)    
    data = "code=0e3Ly5100hMFCQ1SGr000JzTbv1Ly514&aid=%s&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&yk_scene=&_page=&__from=wxapp" % (aid, time)
    res = utils.send_request(url, "", data)
    print(res.text)
    json_data = json.loads(res.text)
    success = json_data["success"]
    if success == "true":
        return json_data["msg"]
    else:
        return ""

def main():

    # 替换为自己的aid，固定值
    aid = "28268434"
    # 替换session_key，每次都要更新
    session_key = "hHAd5x%2F7zLaXa8OH1EzrV0JYC828113ulnDtDxV8mFw%3D"
    # 替换cookie，每次都要更新
    cookie = "_cliid=Hd6Qx3eksd2p7Pdq; undefined=undefined; _faiHeDistictId=62a979690a8b6cde; _faiHeSessionId=62a9796972898187; _faiHeSesPvStep=50; behaviorData=%7B%22cookieVisitIdMap%22%3A%22%7B70001%3A%5C%22b6caf39f981a2b68%5C%22%2C70016%3A%5C%22ab01520382743cf9%5C%22%2C70021%3A%5C%22b53a960298a26526%5C%22%7D%22%2C%22cookieNowVisitId%22%3A%22b6caf39f981a2b68%22%7D"
    
    for i in range(0, 99999):
        # 20点 - 21点，每个小时 2 片场地
        start_time = utils.transform_time_to_millisecond("2023-09-23 20:00:00.000")
        end_time   = utils.transform_time_to_millisecond("2023-09-23 21:00:00.000")
        reserve_badminton(aid, cookie, session_key, start_time, end_time, num=2)

        # # 19点 - 21点，每个小时 1 片场地
        # start_time = utils.transform_time_to_millisecond("2023-09-23 19:00:00.000")
        # end_time   = utils.transform_time_to_millisecond("2023-09-23 21:00:00.000")
        # reserve_badminton(aid, cookie, session_key, start_time, end_time, num=1)

        # sleep 0.5s
        time.sleep(0.5)


if __name__ == "__main__":
    main()