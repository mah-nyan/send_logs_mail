# send_logs_mail
WOWHoneypotのlogをメール送信するpython3スクリプトです!
前日のlogを引っ張ってくるので、00:05等にcronで登録しておくと便利です。
本文にサマリが表示され、圧縮されたファイルの中に、デコードしたlogとcsvが添付されます。
実行するサーバに7zのinstallが必要です。

# mail sample
■2019-04-01のアクセス数は58件でした。

■送信元IPアドレスの数は 51件です。

■メソッドの一覧と件数は以下です。

method GET 60 POST 1 CONNECT 1 Name: path, dtype: int64

■アクセスパス一覧と件数は以下です。

path / 39 /manager/html 4 /favicon.ico 3 /struts2-rest-showcase/orders.xhtml 1 /sitemap.xml 1 /robots.txt 1 /tmUnblock.cgi 1 /index.do 1 /index.action 1 /version 1 /cms1/wp-login.php 1 /cms1//wp-json/wp/v2/users/ 1 /cms1//?author=1 1 /cms/wp-login.php 1 /cms//wp-json/wp/v2/users/ 1 /cms//?author=1 1 //ldskflks 1 /.well-known/security.txt Name: method, dtype: int64

■添付ファイルのpasswordは、以下となっています。

honeypot