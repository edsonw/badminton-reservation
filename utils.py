import re, requests, time
from urllib3.exceptions import InsecureRequestWarning

# 将"2023-09-06 00:00:00.999"转换为毫秒
def transform_time_to_millisecond(time_str) -> int:
    ms = time_str.split(".")[1]
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M:%S.%f")
    time_stamp = int(time.mktime(time_array) * 1000) + int(ms)
    return time_stamp

# 将1693962000000转换为"2023-09-06 00:00:00.000"
def transform_millisecond_to_time(millisecond) -> str:
    millisecond = int(millisecond)
    ms = millisecond % 1000
    time_array = time.localtime(millisecond / 1000)
    time_str = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return time_str + str(ms)

def get_hour_from_timestamp(timestamp) -> int:
    time_array = time.localtime(int(timestamp) / 1000)
    hour = time.strftime("%H", time_array)
    return int(hour)

def get_timestamp() -> int:
    return int(time.time() * 1000)

# 获取当前0点的时间戳
def get_today_timestamp() -> int:
    time_array = time.localtime()
    time_str = time.strftime("%Y-%m-%d", time_array)
    time_array = time.strptime(time_str, "%Y-%m-%d")
    time_stamp = int(time.mktime(time_array) * 1000)
    return time_stamp

def send_request(url, cookie, data):
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

    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    response = requests.post(url, headers=headers, data=data, verify=False)

    return response

