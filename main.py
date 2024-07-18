import utils, json, datetime as new_datetime, threading, time as new_time

from datetime import datetime, time
import re, requests
from urllib3.exceptions import InsecureRequestWarning
import urllib.parse

requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
def send_request(session, url, cookie, data):
    headers = {
        "Host": "m.yk.fkw.com",
        "Connection": "keep-alive",
        "Content-Length": str(len(data)),
        "xweb_xhr": "1",
        "cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8379",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
        "Accept": "*/*",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://servicewechat.com/wxa5a9cfd49709ae9e/44/page-frame.html",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh",
    }

    try:
        session.headers.update({"Cookie": cookie})
        response = session.post(url, data=data, headers=headers, verify=False)
        print(response.text)
        return response
    except Exception as e:
        print(e)
        return None

def reserve_by_hour(session, aid, cookie, session_key, bes_time, end_time, service_id, sku_id, num):
    now = utils.get_timestamp()
    url = "https://m.yk.fkw.com/ajax/api.jsp?cmd=bespeak/add"
    url += "&aid=%s&yid=1&sessionKey=%s" % (aid, session_key)
    url += "&isFromOpen=true&vers=20240530&_grp=a&_t=%s&wx_scene=1257&fromMid=0" % now
    url += "&mgClueReportInfo={\"sourceModule\":70009,\"sourcePath\":0,\"sourceContentType\":0,\"sourceChannel\":-100,\"sourceType\":2}&yk_scene=&_page=reserve/comfirmRecord&__from=wxapp"

    data = "aid=%s&yid=1&note&nextDay=false&besTime=%s&endTime=%s" % (aid, bes_time, end_time)
    data += f"&logicList=%5B%5D&storeId=1&serviceId={service_id}&bespeakNum=1&mgClueReportInfo=%7B%22sourceModule%22%3A70009%2C%22sourcePath%22%3A0%2C%22sourceContentType%22%3A0%2C%22sourceChannel%22%3A-100%2C%22sourceType%22%3A2%7D"
    data += f"&fromMid=0&name=%E5%90%B4%E5%BF%97%E6%96%B0&phone=18328582840&bespeakCustomFields=%7B%7D&skuId={sku_id}&channelId=0&formId=1&itemData=%5B%7B%22itemId%22%3A%2263302%22%2C%22itemValue%22%3A%22%22%7D%5D"

    cross_bes_time_list = []
    for i in range(num):
        start_time = bes_time + i * 3600000
        end_time = start_time + 3600000
        cross_bes_time_list.append({
            "besTime": start_time,
            "endTime": end_time,
            "timeName": "",
            "logicList": []
        })

    data += "&crossBesTimeList=%s" % urllib.parse.quote(json.dumps(cross_bes_time_list))

    data += f"&isUseMemberDiscount=true&itemList=%5B%7B%22type%22%3A1%2C%22price%22%3A0%2C%22subtotal%22%3A0%2C%22num%22%3A{num}%2C%22data%22%3A%7B%22isUseMemberDiscount%22%3Atrue%2C%22serviceId%22%3A{service_id}%2C%22priceType%22%3A0%2C%22skuId%22%3A{sku_id}%2C%22goodsFlag%22%3A1628447953%2C%22goodsPhoto%22%3A%22http%3A%2F%2F28268434.s143i.faiykusr.com%2F2%2F1%2FAI8BCJKvvQ0QAhgAIIDi4p8GKNqDiKkFMIAgOIAg.jpg%22%2C%22memberDiscount%22%3A0%2C%22memberPriceData%22%3A%7B%7D%7D%7D%5D&deductionList=%5B%5D&totalPrice=0&shouldPrice=0&realPrice=0&payType=4&bespeakPay=1&_track=%5B%22home%2Fhome%22%2C%22serviceDetail%2FserviceDetail%22%2C%22reserve%2Fadd%22%2C%22reserve%2FcomfirmRecord%22%5D"
    data += "&_t=%s&_grp=a&__from=wxapp" % now

    res = send_request(session, url, cookie, data)
    print(res.text)
    json_data = json.loads(res.text)
    if "success" in json_data:
        success = json_data["success"]
        if success:
            print("reserve success")
            return 1
        else:
            print("reserve failed")
            return 0
    else:
        return 0

def reserve_badminton(session, aid, cookie, session_key, bes_time, end_time):
    # 免费时段
    service_id = 14
    sku_id = 73

    # 节假日是70 80
    # service_id = 70
    # sku_id = 80

    # 低收费时段
    # service_id = 16
    # sku_id = 71

    # 正常收费时段
    # service_id = 76
    # sku_id = 92

    hour_count = int((end_time - bes_time) / 3600000)

    return reserve_by_hour(session, aid, cookie, session_key, bes_time, end_time, service_id, sku_id, hour_count)


def reserve_thread(aid, cookie, session_key):
    with requests.Session() as session:
        # 预约时间 gap
        today = new_datetime.date.today() + new_datetime.timedelta(days=2)
        day_str = today.strftime("%Y-%m-%d")
        wait_flag = True
        count = 0
        for i in range(999999):
            if wait_flag:
                current_time = new_datetime.date.today()
                target_time = datetime.combine(current_time, time(8, 59, 59, 999))
                wait_until(target_time)
                wait_flag = False
                print(f"等待到 {target_time}")
                print(f"开始预约 {day_str}")
            else:

                new_time.sleep(1) # 捡漏时使用
                start_time = utils.transform_time_to_millisecond(f"{day_str} 9:00:00.000")
                end_time = utils.transform_time_to_millisecond(f"{day_str} 11:00:00.000")
                result = reserve_badminton(session, aid, cookie, session_key, start_time, end_time)
                count = count + result
                #  预约成功了就可以退出了
                if count == 1:
                    break

def wait_until(target):
    """等待直到指定的时间点"""
    while True:
        now = datetime.now()
        # 如果当前时间到达或者超出目标时间，跳出循环
        if now >= target:
            break
        # 这里可以根据你想要的等待精度来选择sleep的时间
        new_time.sleep(0.01)  # 调整时间间隔以便在目标时间快速醒来


def main():
    aid = "28268434"
    session_key = "4u%2B7ooV7XUrux2Idks6i1i8ru2t72E9iJqpJKvFSub4%3D"
    cookie = "_cliid=WYoeFqLHxWgxMdqM; undefined=undefined; behaviorData=%7B%22cookieVisitIdMap%22%3A%22%7B70001%3A%5C%229f4b3263d6d26d8c%5C%22%2C70016%3A%5C%22953cc3423e85cba0%5C%22%2C70021%3A%5C%229f4e40593763bde2%5C%22%2C70040%3A%5C%22c72cf20bcc060302%5C%22%7D%22%2C%22cookieNowVisitId%22%3A%229f4e40593763bde2%22%7D; _faiHeDistictId=63dfb594c58ba2f9; _faiHeSessionId=63dfb594c58b90f5; _faiHeSesPvStep=1095; JSESSIONID=25726008742019A46617B30E5ED4D0B8"
    threads = []
    for i in range(1):  # 10个线程
        thread = threading.Thread(target=reserve_thread, args=(aid, cookie, session_key))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()  # 等待所有线程完成


if __name__ == "__main__":
    main()
