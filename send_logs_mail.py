# -*- coding: utf-8 -*-
#WOWHoneypotの前日のlogをメール送付するpython3スクリプトです。
#本文にはサマリが記載され、加工したlogが圧縮されて届きます。(passwordはhoneypot)
#圧縮時にsubprocessで7zipを呼び出すため、事前にインストールが必要です。
#sudo apt install p7zip-full
#sudo pip3 install pandas
#2019-04-11 mah-nyan
import smtplib
from email.mime.text import MIMEText
from email.utils import formatdate
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import datetime
import re
import os
import csv
from os.path import basename
import base64
import subprocess
from collections import Counter
import pandas as pd

LOGIN_ADDRESS = 'your.smtp.server@login.address'
ENVELOPE_ADDRESS = 'wowhoneypot@your.domain'
MY_PASSWORD = 'foobar'
TO_ADDRESS = 'your@gmail.com'
SUBJECT = 'WOWHoneypot1号のDailylog'
yestarday = datetime.date.today() - datetime.timedelta(1)

def create_file():
    try:
        
        accesslog = open('/opt/wow/WOWHoneypot/log/access_log')
        lines = accesslog.readlines()
        accesslog.close

        logcount = 0
        rawdata = "■アクセスlogのrawdataは以下となってます。\n\n"
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                logcount += 1
                rawdata += "-=-=" + str(logcount) + "件目のlog=-=-\n\n"
                rawdata += line[:-1]
                bunkatsu = line.rsplit(" ", 1)
                decdata = (base64.decodestring(bunkatsu[-1].encode("ascii")).decode("utf8"))
                rawdata += ("\n\n" + str(decdata) + "\n\n")

        ac_log = str()
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0:
                bunkatsu2 = line.rsplit(" ", 1)
                decdata2 = (base64.decodestring(bunkatsu2[-1].encode("ascii")).decode("utf8"))
                ac_log += line.rsplit(" ", 1)[0] + decdata2  

        all_iplist =[]
        for line in lines:
            ###################################################################↓除外したいIPアドレス。例えば確認時にアクセスする自分のGIP等
            if line.find(yestarday.strftime("%Y-%m-%d")) >= 0 and line.find("1.2.3.4") < 0 :
                all_ips = re.search("(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}(([1-9]?[0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\s)", line)
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
                    huntingdata += line[:-1]
                    huntingdata += "\n\n"
        else:
            huntingdata = ("■hunting.logは生成されていません。\n\n")

        body = "■" + yestarday.strftime("%Y-%m-%d") + "のアクセス数は" + str(logcount) + "件でした。\n\n"+ "■送信元IPアドレスの数は\n"\
        + str(len(unique_iplist)) + "件です。\n\n"

        if not os.path.exists("./log/"):
            os.mkdir("./log/")
        
        csv = open("./log/access_" + yestarday.strftime("%Y-%m-%d") + ".log", "w")
        csv.write(ac_log)
        csv.close

        f = open("./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".log", "w")
        f.write(huntingdata + rawdata)
        f.close
        
        return body

    except Exception as e:
        body = str(e)
        print = str(e)
        return body


def create_csv(body): 
    try:
        arg1 = "log/access_" + yestarday.strftime("%Y-%m-%d") + ".log"
        log_file = open("./" + arg1)
        lines = log_file.readlines()
        log_file.close
        csvdata = [["date", "time", "src_ip", "method", "path"]]
        for line in lines:
            date = re.search ("\d{4}-\d{2}-\d{2}", line)
            time = re.search ("\d{2}:\d{2}:\d{2}", line)
            srcip = re.search ("]\s\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}", line)
            method = re.search ("(?<=\s\")\w+", line)
            uri = re.search ("\s/\s|\s(/[\w/:%#\$&\?\(\)~\.\\\&\[\]=\+\-]+)(?=\sHTTP/\d\.\d\")", line)
            uri2 = re.search ("\s(\w+[\w/:%#\$&\?\(\)~\.\\\&\[\]=\+\-]+)(?=\sHTTP/\d\.\d\")", line)
            uri3 = re.search ("\s\s(?=HTTP/\d\.\d\")", line)

            if uri is not None:
                rawuri = str(uri.group()).lstrip( )
                rawsrcip = str(srcip.group())
                csvdata += [[date.group(), time.group(), rawsrcip.replace("] ", ""), method.group(), rawuri]]

            if uri2 is not None:
                rawuri2 = str(uri2.group()).lstrip( )
                rawsrcip = str(srcip.group())
                csvdata += [[date.group(), time.group(), rawsrcip.replace("] ", ""), method.group(), rawuri2]]

            if uri3 is not None:
                rawuri3 = str(uri3.group()).lstrip( )
                rawsrcip = str(srcip.group())
                csvdata += [[date.group(), time.group(), rawsrcip.replace("] ", ""), method.group(), rawuri3]]
        
        if not os.path.exists("./log/"):
            os.mkdir("./log/")            
        
        with open('./' + arg1 + ".csv", "w") as file:
            writer = csv.writer(file, lineterminator='\n')
            writer.writerows(csvdata)

        return body

    except Exception as e:
        csvdata += [["error", "error", "error", "error", str(e)]]
        print (str(e))
        body += "※csv作成時にエラーが発生しています。\n\n"
        return body


def log_analyze(body):
    try:
        log_analyzed = str()
        arg1 = "log/access_" + yestarday.strftime("%Y-%m-%d") + ".log"
        df = pd.read_csv('./' + arg1 + ".csv",sep=",")
        df.columns = ["date", "time", "srcip", "method", "path"]
               
        df_by_method = df.groupby("method")["path"].count().sort_values(ascending=False)
        log_analyzed += "■メソッドの一覧と件数は以下です。\n\n"
        log_analyzed += str(df_by_method) + "\n\n"
        
        df_by_uri = df.groupby("path")["method"].count().sort_values(ascending=False)
        log_analyzed += "■アクセスパス一覧と件数は以下です。\n\n"
        log_analyzed += str(df_by_uri) + "\n\n"
        
        body += log_analyzed

        return body

    except Exception as e:
        body += "※log分析時にエラーが発生しています。\n\n"
        return body


def compress_files(body):
    try:
        cmd = "7z a -phoneypot " + "./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".7z " + "./log/access_" \
            + yestarday.strftime("%Y-%m-%d") + ".log " + "./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".log " \
                + "./log/access_" + yestarday.strftime("%Y-%m-%d") + ".log.csv"

        subprocess.run(cmd.split())

        body += "■添付ファイルのpasswordは、以下となっています。\n\nhoneypot\n\n"
        return body

    except Exception as e:
        body += "※ファイル圧縮時にエラーが発生しています。\n\n"
        return body


def create_message(from_addr, to_addr, subject, body, mine):
    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Date'] = formatdate()

    body = MIMEText(body)
    msg.attach(body)

    path = "./log/honeypot_" + yestarday.strftime("%Y-%m-%d") + ".7z"
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
    body = compress_files(log_analyze(create_csv(create_file())))
    mine={'type':'text','subtype':'comma-separated-values'}
    msg = create_message(ENVELOPE_ADDRESS, to_addr, subject, body, mine)
    send(ENVELOPE_ADDRESS, to_addr, msg)