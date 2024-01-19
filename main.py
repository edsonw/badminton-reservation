
import utils, json, time, datetime, threading

def send_request(url, cookie, data):
    try:
        res = utils.send_request(url, cookie, data)
    except Exception as e:
        print(e)
        return

    print(res.text)

    return res

def reserve_one_hour(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num):
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
    
    return send_request(url, cookie, data)

def reserve_two_hour(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num):
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
    
    return send_request(url, cookie, data)

def reserve_badminton(aid, cookie, session_key, bes_time, end_time, num = 1):
    service_id = 14
    sku_id = 73

    # 节假日是70 80
    # service_id = 70
    # sku_id = 80
    count = int((end_time - bes_time ) / 3600000)
    if count == 1:
        return reserve_one_hour(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num)
    elif count == 2:
        return reserve_two_hour(aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num)

def reserve_thread(aid, cookie, session_key):
    # 获取当前时间的年月日，再加2天
    today = datetime.date.today() + datetime.timedelta(days=2)
    day_str = today.strftime("%Y-%m-%d")
    for i in range(0, 99999):
        now = datetime.datetime.now()
        if now.hour < 9 and now.minute < 59 and now.second < 30:
            time.sleep(0.1)
            continue

        # start_time = utils.transform_time_to_millisecond(day_str + " 15:00:00.000")
        # end_time   = utils.transform_time_to_millisecond(day_str + " 17:00:00.000")
        start_time = utils.transform_time_to_millisecond(day_str + " 09:00:00.000")
        end_time   = utils.transform_time_to_millisecond(day_str + " 11:00:00.000")
        reserve_badminton(aid, cookie, session_key, start_time, end_time, num=1)

        time.sleep(5)

def main():

    # 替换为自己的aid，固定值
    aid = "28268434"
    # 替换session_key，每次都要更新
    session_key = "iouKmfUkIOT2rwomIlM58cF2dmSoZk7ml7VkEX%2B%2FrfM%3D"
    # 替换cookie，每次都要更新
    cookie = "_cliid=wX0usF_LbJdimyUY; undefined=undefined; _faiHeDistictId=632279fa740bd790; behaviorData=%7B%22cookieVisitIdMap%22%3A%22%7B70001%3A%5C%22f603274bd192e24f%5C%22%2C70021%3A%5C%22fb26817a293dd0d9%5C%22%7D%22%2C%22cookieNowVisitId%22%3A%22fb26817a293dd0d9%22%7D; _faiHeSessionId=632279fad50be940; _faiHeSesPvStep=65"

    # 创建10个线程，执行reserve_thread函数
    for i in range(10):
        thread = threading.Thread(target=reserve_thread, args=(aid, cookie, session_key))
        thread.start()

    # 暂停主线程，防止程序退出
    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()