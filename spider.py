from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq
import time
from functions import send_email
import os

class Spider:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.browser = webdriver.Chrome(service_args=['--load-images=false', '--disk-cache=true'])
        self.browser.set_window_size(1400, 900)
        self.wait = WebDriverWait(self.browser, 10)

    def login(self):
        print('start to login')
        url = 'https://rcgy.zjhui.net/'
        self.browser.get(url)
        login_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login')))
        login_btn.click()
        tel = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_tel')))
        tel.send_keys(self.username)
        password = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_password')))
        password.send_keys(self.password)
        login_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#login_btn')))
        time.sleep(2)
        login_btn.click()
        goto_btn = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#imgloginback')))
        if goto_btn:
            return True
        return False            

    def get_waiting_record(self):
        print('start to get waiting record')
        url = 'https://rcgy.zjhui.net/System/WaitingRecord.aspx'
        self.browser.get(url)
        self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#ctl00_ctl00_ctl00_main_main_main_palPT')))
        html = self.browser.page_source
        doc = pq(html)
        # if the selector is `#ctl00_ctl00_ctl00_main_main_main_palPT > table`
        # it can't get any value.
        trs = doc('#ctl00_ctl00_ctl00_main_main_main_palPT').items()
        arr = []
        # I don't konw why the append operation is not excepted.
        for tr in trs:
            for td in tr.items():
                arr.append(td.text())
        arr = arr[0].split('\n')
        record = {
            'username': arr[21],
            'order_number': arr[20],
            'apply_time': arr[22],
            'building': arr[23],
            'price': arr[25] + arr[26],
            'company_state': arr[28],
            'appy_state': arr[29],
            'adjust': arr[30],
            'rank': arr[31],
        }
        print(record)
        return record

    def start(self):
        print('spider is starting')
        if self.login():
            time.sleep(2)
            return self.get_waiting_record()
        else:
            print('login failed')


if __name__ == "__main__":
    zj_username = os.environ['ZJ_USERNAME']
    zj_pwd = os.environ['ZJ_PWD']
    print('using username(%s) and password (%s) to login zj-system' % (zj_username, zj_pwd))
    spider = Spider(zj_username, zj_pwd)
    record = spider.start()

    email_stmp_server = os.environ['EMAIL_SMTP_SERVER']
    email_sender = os.environ['EMAIL_SENDER']
    email_sender_pwd = os.environ['EMAIL_SENDER_PWD']
    email_receiver = os.environ['EMAIL_RECEIVER']
    print('using stmp server (%s), sender email (%s), sender password (%), receiver (%s)' %
     (email_stmp_server, email_sender, email_sender_pwd, email_receiver))
    send_email(email_stmp_server, email_sender, email_sender_pwd, [email_receiver], record)