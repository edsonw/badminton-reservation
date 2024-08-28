import requests
import json
import threading
from datetime import datetime, time, timedelta
import datetime as new_datetime, time as new_time

# 定义一个函数来发送请求
def send_request(times_list,Authorization, venue_num, reverse_time, venue_id, venue_money):
    headers = {
        'Host': 'www.zwcdata.com',
        'Authorization': Authorization,
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.50(0x18003239) NetType/4G Language/zh_CN',
        # todo： 这里确认一下是否不同的账户是不同的？
        'Referer': 'https://servicewechat.com/wx777adf4e834206b4/6/page-frame.html'
    }

    data = {
        'isCoach': '0',
        'type': 0,
        'venueName': '高新体育中心',
        'startTime': reverse_time,
        'times': times_list,  # 使用动态的times列表
        'venueId': venue_id,
        'venuetypeId1': 29,
        'venuetypeId2': '3'+venue_num,
        'venueMoney': venue_money,
        'venuetypeName1': '羽毛球',
        'venuetypeName2': venue_num+'号'
    }

    url = 'https://www.zwcdata.com/ly/api/venueOrder'

    wait_flag = True
    for i in range(999999):
        if wait_flag:
            current_time = new_datetime.date.today()
            target_time = datetime.combine(current_time, time(8, 59, 59, 999))
            wait_until(target_time)
            wait_flag = False
            print(f"等待到 {target_time}")
        else:
            # new_time.sleep(1) # 捡漏时使用
            response = requests.post(url, headers=headers, data=json.dumps(data))
            print(response.text)
            json_data = json.loads(response.text)
            if json_data["code"] == 200:
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

# 工具函数：转换开始和结束时间为半小时间隔的时间列表
def create_times_list(start_time, end_time):
    start_dt = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    times_list = []

    while start_dt < end_dt:
        end_interval_dt = start_dt + timedelta(minutes=30)
        times_list.append(f"{start_dt.strftime('%H:%M')}-{end_interval_dt.strftime('%H:%M')}")
        start_dt = end_interval_dt
    return times_list

# 线程运行的主函数
def run_thread(authorization_token, start_time, end_time, venue_num, reverse_time, venue_id, venue_money):
    times_list = create_times_list(start_time, end_time)

    send_request(times_list, authorization_token, venue_num, reverse_time, venue_id, venue_money)


if __name__ == '__main__':

    # 预约日期
    today = new_datetime.date.today() + new_datetime.timedelta(days=2)
    reverse_time = today.strftime("%Y-%m-%d")
    # 定义所需的times列表
    start_time_user = "9:00"
    end_time_user = "12:00"
    # 预约场地id，一个场地多个线程就填多个id
    venue_nums = ['2','3','4']
    # 目前看是固定值
    venue_id = '3'
    # 付费金额(分) 自己算
    venue_money = 0 * 100

    # 抓包替换为自己的
    authorization_token= 'Bearer eyJhbGciOiJIUzUxMiJ9.eyJsb2dpbl9hcGlfdXNlcl9rZXkiOiJlYmQ1NTRkNi1iNTMwLTQwNzAtODAzZS1hOGE2MmQ0OGFhODgifQ.kWm_o7pRMzgRDSTwBxBDG53OwHcGAvLFWyGiQf4Uy5PC_mDNNHuZ3_7MfmgvzjNMRp-ZAn9pxSzRpmD96cxZTA'
    # 调用函数发送请求

    threads = []
    for venue_num in venue_nums:
        thread = threading.Thread(target=run_thread, args=(authorization_token, start_time_user,
                                                           end_time_user, venue_num, reverse_time, venue_id, venue_money))
        threads.append(thread)
        thread.start()

    # 主线程继续执行，或者等待子线程结束（根据实际情况）
    for thread in threads:
        thread.join()
