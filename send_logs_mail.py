# -*- coding: utf-8 -*-
#WOWHoneypotの前日のlogをメール送付するpython3スクリプトです。
#本文にはサマリが記載され、加工したlogが圧縮されて届きます。
#2019-04-04 mah-nyan
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import datetime
import re
import os
from os.path import basename
import base64
import zipfile
from collections import Counter

LOGIN_ADDRESS = 'your.smtp.server@login.address'
ENVELOPE_ADDRESS = 'wowhoneypot@your.domain'
MY_PASSWORD = 'foobar'
TO_ADDRESS = 'your@gmail.com'
SUBJECT = 'WOWHoneypot1号のDailylog'
yestarday = datetime.date.today() - datetime.timedelta(1)

def create_body():
    try:
        
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
        rawdata = "■アクセスlogのrawdataは以下となってます。\n\n"
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                logcount += 1
                if line.find("\"GET") >= 0:
                    getcount += 1
                if line.find("\"POST") >= 0:
                    postcount += 1
                if line.find("\"HEAD") >= 0:
                    headcount += 1
                if line.find("\"CONNECT") >= 0:
                    connectcount += 1
                if line.find("\"PUT") >= 0:
                    putcount += 1
                if line.find("\"PROPFIND") >= 0:
                    propfindcount += 1    
                rawdata += "-=-=" + str(logcount) + "件目のlog=-=-\n\n"
                rawdata += line[:-1]
                bunkatsu = line.rsplit(" ", 1)
                decdata = (base64.decodestring(bunkatsu[-1].encode("ascii")).decode("utf8"))
                rawdata += ("\n\n" + str(decdata) + "\n\n")

        ac_csv = str()
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                bunkatsu2 = line.rsplit(" ", 1)
                decdata2 = (base64.decodestring(bunkatsu2[-1].encode("ascii")).decode("utf8"))
                ac_csv += line.rsplit(" ", 1)[0] + decdata2  

        all_iplist =[]
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0 :
                all_ips = re.search("(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])", line)
                all_iplist.append(all_ips.group())
                unique_iplist = list(dict.fromkeys(all_iplist))

        all_ipcount = Counter(all_iplist)
        ip_data = "■送信元ipアドレスの一覧と件数は以下となります。\n\n"
        for ip_key in all_ipcount.keys():
            ip_val = all_ipcount[ip_key]
            ip_data += str(ip_key) + "・・・" + str(ip_val) + "件\n\n"

        if os.path.exists("/opt/wow/WOWHoneypot/log/hunting.log"): 
            with open('/opt/wow/WOWHoneypot/log/hunting.log', "r") as huntinglog:
                lines2 = huntinglog.readlines()
                huntinglog.close

            huntingdata = "■huntinglogのrawdataは以下となってます。\n\n"
            for line in lines2:
                ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
                if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                    huntingdata += line[:-1]
                    huntingdata += "\n\n"
        else:
            huntingdata = ("■hunting.logは生成されていません。\n\n")

        body = "■" + yestarday.strftime("%Y-%m-%d") + "のアクセス数は" + str(logcount) + "件でした。\n\n"+ "■送信元IPアドレスの数は\n"\
        + str(len(unique_iplist)) + "件です。\n\n" + "■メソッドの種別は以下です。\n\n" + " GET・・" + str(getcount) + "件\n" \
        + " PUT・・" + str(putcount) + "件\n" + " POST・・" + str(postcount) + "件\n" + " HEAD・・" + str(headcount) + "件\n" \
        + " CONNECT・・" + str(connectcount) + "件\n" +  " PROFFIND・・" + str(propfindcount) + "件\n" + " その他・・" \
        + str(logcount - (getcount + putcount + postcount + headcount + connectcount + propfindcount)) + "件\n\n" + ip_data

        if not os.path.exists("./log/"):
            os.mkdir("./log/")
        
        csv = open("./log/access_" + yestarday.strftime("%Y-%m-%d") + ".log", "w")
        csv.write(ac_csv)
        csv.close

        f = open("./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".log", "w")
        f.write(huntingdata + rawdata)
        f.close

        compfile = zipfile.ZipFile("./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".zip", "w", zipfile.ZIP_LZMA)
        compfile.write("./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".log")
        compfile.write("./log/access_" + yestarday.strftime("%Y-%m-%d") + ".log")
        compfile.close()

        return body
    except Exception as e:
        body = str(e)
        print = str(e)
        return body


def create_message(from_addr, to_addr, subject, body, mine):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    body = MIMEText(body)
    msg.attach(body)

    path = "./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".zip"
    with open(path, "rb") as f:
        part = MIMEApplication(
            f.read(),
            Name=basename(path)
        )
 
    part['Content-Disposition'] = 'attachment; filename="%s"' % basename(path)
    msg.attach(part)

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
    mine={'type':'text','subtype':'comma-separated-values'}
    msg = create_message(ENVELOPE_ADDRESS, to_addr, subject, body, mine)
    send(ENVELOPE_ADDRESS, to_addr, msg)