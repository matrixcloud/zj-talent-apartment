import time
import smtplib
from email.message import EmailMessage

def send_email(stmp_server, sender, sender_pwd, receivers, record):
    date_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    msg = EmailMessage()
    msg['Subject'] = '张江人才公寓申请报告 (%s)' % date_time
    msg['From'] = sender
    msg['To'] = receivers
    msg.set_content("""
        【Apply Number】：%s
        【Apply Person】：%s
        【Current Rank】：%s
        【Appy Date】：%s
        【Room Type】：%s
        【Price】：%s
        【Company State】：%s
        【Apply State】：%s
    """ % (
        record['order_number'],
        record['username'],
        record['rank'],
        record['apply_time'],
        record['building'],
        record['price'],
        record['company_state'],
        record['appy_state']
    ))
    s = smtplib.SMTP_SSL(stmp_server, 465)
    s.login(sender, sender_pwd)
    s.send_message(msg)
    s.quit()