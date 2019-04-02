# send_logs_mail
WOWHoneypotのlogをメール送信するpython3スクリプトです!

前日のlogを引っ張ってくるので、00:05等にcronで登録しておくと便利です。

#sample
■2019-04-01のアクセス数は58件でした。

■送信元IPアドレスの数は 51件です。

■メソッドの種別は以下です。

GET・・54件
PUT・・0件
POST・・0件
HEAD・・1件
CONNECT・・3件
PROFFIND・・0件
その他・・0件

■hunting.logは生成されていません。

■送信元IPアドレスの一覧は以下となります。

['1.2.3.4', ‘5.6.7.8’]

■アクセスlogのrawdataは以下となってます。

-=-=1件目のlog=-=-

[2019-04-01 00:02:59+0900] 1.2.3.4 10.20.30.40:8080 “GET / HTTP/1.1” 200 False R0VUIC8gSFRUUC8xLjEKSG9zdDogMTMzLjE2Ny4xMDguMTUyOjgwODAKVXNlci1BZ2VudDogTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzUyLjAuMjc0My4xMTYgU2FmYXJpLzUzNy4zNgpDb250ZW50LUxlbmd0aDogMAoK

GET / HTTP/1.1 Host: 10.20.30.40:8080 User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Content-Length: 0

-=-=2件目のlog=-=-

[2019-04-01 00:07:25+0900] 5.6.7.8 10.20.30.40:8080 “GET / HTTP/1.1” 200 False R0VUIC8gSFRUUC8xLjEKSG9zdDogMTMzLjE2Ny4xMDguMTUyOjgwODAKVXNlci1BZ2VudDogTW96aWxsYS81LjAgKFdpbmRvd3MgTlQgNi4xOyBXT1c2NCkgQXBwbGVXZWJLaXQvNTM3LjM2IChLSFRNTCwgbGlrZSBHZWNrbykgQ2hyb21lLzUxLjAuMjcwNC4xMDMgU2FmYXJpLzUzNy4zNgpDb250ZW50LUxlbmd0aDogMAoK

GET / HTTP/1.1 Host: 10.20.30.40:8080 User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36 Content-Length: 0