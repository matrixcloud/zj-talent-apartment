# Zhangjiang Talent Apartment Notifier

This program will query your waiting record of ZhangJiang Talent Apartment and send a email to you.

## How to use

you can use it via `crontab`, for example.

```bash
0 * * * 0,6 ZJ_USERNAME=xxx ZJ_PWD=xxx EMAIL_SMTP_SERVER=xxx EMAIL_SENDER=xxx EMAIL_SENDER_PWD=xxx EMAIL_RECEIVER=xxx python3 spider.py
```

> It means this spider will start every Saturday and Sunday.

## Environment Variables

- ZJ_USERNAME
- ZJ_PWD
- EMAIL_SMTP_SERVER
- EMAIL_SENDER
- EMAIL_SENDER_PWD
- EMAIL_RECEIVER

```bash
export ZJ_USERNAME=xxx \
ZJ_PWD=xxx \
EMAIL_SMTP_SERVER=xxx \
EMAIL_SENDER=xxx \
EMAIL_SENDER_PWD=xxx \
EMAIL_RECEIVER=xxx \
```