import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime, timezone
import json

logging.basicConfig(level=logging.DEBUG,
                    filename="logs",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s - [%(levelname)s] -  %(message)s',
                    datefmt='%H:%M:%S')
LOCAL_TIMEZONE = datetime.now(timezone.utc).astimezone().tzinfo
logging.info(f"LOCAL TIMEZONE IS {LOCAL_TIMEZONE}")


class Credentials:

    def __init__(self, values):
        self.LOGIN_DATA = values
        self.s = requests.Session()
        self.auth_moodle()

    def auth_moodle(self):
        login, password, url = self.LOGIN_DATA.values()
        r_1 = self.s.get(url=url + "/login/index.php")
        r_1 = get_bs_object(r_1.text)
        token = r_1.find('input', {'name': 'logintoken'}).get('value')
        logging.debug(f"LOGINTOKEN IS {token}")
        payload = {'anchor': '',
                   'logintoken': token,
                   'username': login,
                   'password': password,
                   'rememberusername': 1}
        r_2 = self.s.post(url=url + "/login/index.php", data=payload)

    def get_tasks(self):
        logging.debug("Finished auth")
        login, password, url_domain = self.LOGIN_DATA.values()
        board = self.s.get(url=url_domain + "/my/index.php")
        board = get_bs_object(board.text)
        sesskey = board.find('input', {'name': 'sesskey'}).get('value')
        logging.debug(f"SESSION KEY IS {sesskey}")
        timesort = get_timesort()
        logging.debug(timesort)
        payload = [{"index": 0,
                    "methodname": "core_calendar_get_action_events_by_timesort",
                    "args": {"limitnum": 12,
                             "timesortfrom": timesort[0],
                             "timesortto": timesort[1],
                             "limittononsuspendedevents": True}
                    }]
        board = self.s.post(url=url_domain + f"/lib/ajax/service.php?sesskey={sesskey}&info=core_course_get_enrolled_courses_by_timeline_classification", json=payload)
        board = board.json()[0].get("data").get("events")
        ### Temporary for debug
        line = []
        for elem in board:
            line.append(elem.get("name"))
            line.append(epoch_to_readable(elem.get("timestart")))
        with open('logs.txt', 'w', encoding='utf-8') as f:
            json.dump(board, f, ensure_ascii=False, indent=4)
        f.close()
        return '\n'.join(line)

def get_timesort():
    current_time = datetime.now(timezone.utc).timestamp()
    current_time = int(current_time) - 3600    # 1 hour offset - just in case
    offset = 7776000
    return current_time, current_time + offset

def get_bs_object(response: str):
    return BeautifulSoup(response, "html.parser")


def epoch_to_readable(value):
    return datetime.fromtimestamp(value, LOCAL_TIMEZONE).strftime('%Y-%m-%d %H:%M:%S')


