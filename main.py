
import utils, json, random, time

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

def reserve(aid, cookie, session_key, bes_time, service_id, sku_id, count = 1):
    now = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/api.jsp?cmd=bespeak/add"
    url += "&aid=%s&yid=1&sessionKey=%s" % (aid, session_key)
    url += "&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&fromMid=0" % now
    url += "&mgClueReportInfo={\"sourceModule\":70009,\"sourcePath\":0,\"sourceContentType\":0,\"sourceChannel\":-100,\"sourceType\":2}&yk_scene=&_page=reserve/comfirmRecord&__from=wxapp"
    
    end_time = int(bes_time) + 3600000 * count
    data = "aid=%s&yid=1&note&nextDay=false&besTime=%s&endTime=%s" % (aid, bes_time, end_time)
    data += f"&logicList=%5B%5D&storeId=1&serviceId={service_id}&bespeakNum=1&mgClueReportInfo=%7B%22sourceModule%22%3A70009%2C%22sourcePath%22%3A0%2C%22sourceContentType%22%3A0%2C%22sourceChannel%22%3A-100%2C%22sourceType%22%3A2%7D"
    data += f"&fromMid=0&name=%E9%99%88%E5%85%88%E7%94%9F&phone=18180890476&bespeakCustomFields=%7B%7D&skuId={sku_id}&channelId=0&formId=1&itemData=%5B%7B%22itemId%22%3A%2263302%22%2C%22itemValue%22%3A%22%22%7D%5D"
    data += "&crossBesTimeList=[{\"besTime\":%s,\"endTime\":%s,\"timeName\":\"\",\"logicList\":[]}]" % (bes_time, end_time)
    data += f"&isUseMemberDiscount=true&itemList=%5B%7B%22type%22%3A1%2C%22price%22%3A0%2C%22subtotal%22%3A0%2C%22num%22%3A1%2C%22data%22%3A%7B%22isUseMemberDiscount%22%3Atrue%2C%22serviceId%22%3A{service_id}%2C%22priceType%22%3A0%2C%22skuId%22%3A{sku_id}%2C%22goodsFlag%22%3A1628447953%2C%22goodsPhoto%22%3A%22http%3A%2F%2F28268434.s143i.faiykusr.com%2F2%2F1%2FAI8BCJKvvQ0QAhgAIIDi4p8GKNqDiKkFMIAgOIAg.jpg%22%2C%22memberDiscount%22%3A0%2C%22memberPriceData%22%3A%7B%7D%7D%7D%5D&deductionList=%5B%5D&totalPrice=0&shouldPrice=0&realPrice=0&payType=4&bespeakPay=1&_track=%5B%22home%2Fhome%22%2C%22serviceDetail%2FserviceDetail%22%2C%22reserve%2Fadd%22%2C%22reserve%2FcomfirmRecord%22%5D"
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

def reserve_badminton(aid, cookie, session_key, bes_time, count = 1):
    return reserve(aid, cookie, session_key, bes_time, 70, 80, count)

def reserve_tabletennis(aid, cookie, session_key, bes_time, count = 1):
    return reserve(aid, cookie, session_key, bes_time, 72, 84, count)


#https://m.yk.fkw.com/ajax/myueke_h.jsp?cmd=getSessionKey&aid=28268434&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=1693969715244&wx_scene=1257&yk_scene=&_page=&__from=wxapp
def get_session_key(aid):
    time = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/myueke_h.jsp?cmd=getSessionKey"
    url += "&aid=%s&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&yk_scene=&_page=&__from=wxapp" % (aid, time)    
    data = "code=0e3Ly5100hMFCQ1SGr000JzTbv1Ly517&aid=%s&yid=1&isFromOpen=true&vers=20230831&_grp=a&_t=%s&wx_scene=1257&yk_scene=&_page=&__from=wxapp" % (aid, time)
    res = utils.send_request(url, data)
    print(res.text)
    json_data = json.loads(res.text)
    success = json_data["success"]
    if success == "true":
        return json_data["msg"]
    else:
        return ""

def main():

    print("Hello World!")
    aid = "28268434"
    # session_key = get_session_key(aid)
    session_key = "%2FuUUQfcTolnOpxh48fowLQRwCp4Q1ckB2WBM5Ogshmg%3D"
    cookie = "_cliid=rG9E61uRehbkHgV5; undefined=undefined; behaviorData=%7B%22cookieVisitIdMap%22%3A%22%7B70001%3A%5C%229252e1374ab48428%5C%22%2C70021%3A%5C%229252e4075939e9f5%5C%22%7D%22%2C%22cookieNowVisitId%22%3A%229252e4075939e9f5%22%7D; _faiHeDistictId=62a48f74264bd006; _faiHeSessionId=62a48f746e0be870; _faiHeSesPvStep=32"
    
    # manully set time
    # time = utils.transform_time_to_millisecond("2023-09-17 19:00:00.000")
    # reserve_badminton(aid, cookie, session_key, time, 2)
    # time = utils.transform_time_to_millisecond("2023-09-17 19:00:00.000")
    # reserve_badminton(aid, cookie, session_key, time, 1)
    # time = utils.transform_time_to_millisecond("2023-09-17 20:00:00.000")
    # reserve_badminton(aid, cookie, session_key, time, 1)
    # time = utils.transform_time_to_millisecond("2023-09-17 18:00:00.000")
    # reserve_badminton(aid, cookie, session_key, time, 1)
    # time = utils.transform_time_to_millisecond("2023-09-17 21:00:00.000")
    # reserve_badminton(aid, cookie, session_key, time, 1)

    for i in range(0, 999999):
        today = utils.get_today_timestamp()
        for i in range(0, 3):
            bes_time = today + 86400000 * i
            print("query badminton: " + utils.transform_millisecond_to_time(bes_time))
            time_list = query_badminton(aid, cookie, session_key, bes_time)
            for time_item in time_list:
                # < 18:00:00
                if utils.get_hour_from_timestamp(time_item) < 19:
                    continue
                print("reserve badminton ready: " + utils.transform_millisecond_to_time(time_item))
                reserve_badminton(aid, cookie, session_key, time_item)

            # print("query tabletennis: " + utils.transform_millisecond_to_time(bes_time))
            # time_list = query_tabletennis(aid, cookie, session_key, bes_time)
            # for time_item in time_list:
            #     # < 18:00:00
            #     if utils.get_hour_from_timestamp(time_item) < 19:
            #         continue
            #     print("reserve tabletennis ready: " + utils.transform_millisecond_to_time(time_item))
            #     reserve_tabletennis(aid, cookie, session_key, time_item)
        
        sleep_time = random.randint(0, 20)
        print("sleep %d seconds" % sleep_time)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()