# send_logs_mail
WOWHoneypotのlogをメール送信するpython3スクリプトです!
前日のlogを引っ張ってくるので、00:05等にcronで登録しておくと便利です。
本文にサマリが表示され、圧縮されたファイルの中に、デコードしたlogが添付されます。

# mail sample
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

■送信元ipアドレスの一覧と件数は以下となります。

1.2.3.4・・・2件

11.22.33.44・・・16件

10.20.30.40・・・1件