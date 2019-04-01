import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
import datetime
import re
import os

LOGIN_ADDRESS = 'your.smtp.server@login.address'
ENVELOPE_ADDRESS = 'wowhoneypot@your.domain'
MY_PASSWORD = 'foobar'
TO_ADDRESS = 'your@gmail.com'
SUBJECT = 'WOWHoneypot1号のDailylog'


def create_body():
    try:
        yestarday = datetime.date.today() - datetime.timedelta(1)
        accesslog = open('/opt/wow/WOWHoneypot/log/access_log')
        lines = accesslog.readlines()
        accesslog.close

        logcount = 0
        getcount = 0
        putcount = 0
        postcount = 0
        headcount = 0
        connectcount = 0
        propfindcount = 0

        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("GET") >= 0:
                getcount += 1
        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("POST") >= 0:
                postcount += 1
        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("HEAD") >= 0:
                headcount += 1
        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("CONNECT") >= 0:
                connectcount += 1
        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("PUT") >= 0:
                putcount += 1
        for line in lines:
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("PROPFIND") >= 0:
                propfindcount += 1

        rawdata = "■アクセスlogのrawdataは以下となってます。\n\n"
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                rawdata += line[:-1]
                rawdata += "\n\n"
                logcount += 1

        
        all_iplist =[]
        #unique_iplist =[]

        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0 :
                all_ips = re.search("(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])", line)
                all_iplist.append(all_ips.group())
                unique_iplist = list(dict.fromkeys(all_iplist))


        if os.path.exists("/opt/wow/WOWHoneypot/log/hunting.log"): 
            with open('/opt/wow/WOWHoneypot/log/hunting.log', "r") as huntinglog:
                lines2 = huntinglog.readlines()
                huntinglog.close

            huntingdata = "■huntinglogのrawdataは以下となってます。\n\n"
            for line in lines2:
                ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
                if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                    rawdata += line[:-1]
                    rawdata += "\n\n"
        else:
            huntingdata = ("■hunting.logは生成されていません。\n\n")


        body = "■" + yestarday.strftime("%Y-%m-%d") + "のアクセス数は" + str(logcount) + "件でした。\n\n"+ "■送信元IPアドレスの数は\n"\
        + str(len(unique_iplist)) + "件です。\n\n" + "■メソッドの種別は以下です。\n\n" + " GET・・" + str(getcount) + "件\n" \
        + " PUT・・" + str(putcount) + "件\n" + " POST・・" + str(postcount) + "件\n" + " HEAD・・" + str(headcount) + "件\n" \
        + " CONNECT・・" + str(connectcount) + "件\n" +  " PROFFIND・・" + str(propfindcount) + "件\n" + " その他・・" \
        + str(logcount - (getcount + putcount + postcount + headcount + connectcount + propfindcount)) + "件\n\n" \
        + huntingdata + "■送信元IPアドレスの一覧は以下となります。\n\n" + str(unique_iplist) + "\n\n" + rawdata
        return body
    except Exception as e:
        body = str(e)
        return body


def create_message(from_addr, to_addr, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()
    return msg


def send(from_addr, to_addrs, msg):
    smtpobj = smtplib.SMTP('your.smtp.server', 587)
    smtpobj.ehlo()
    smtpobj.starttls()
    smtpobj.ehlo()
    smtpobj.login(LOGIN_ADDRESS, MY_PASSWORD)
    smtpobj.sendmail(from_addr, to_addrs, msg.as_string())
    smtpobj.close()


if __name__ == '__main__':

    to_addr = TO_ADDRESS
    subject = SUBJECT
    body = create_body()

    msg = create_message(ENVELOPE_ADDRESS, to_addr, subject, body)
    send(ENVELOPE_ADDRESS, to_addr, msg)