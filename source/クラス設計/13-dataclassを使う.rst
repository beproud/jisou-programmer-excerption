==================
13:dataclassを使う
==================

クラス化したときの問題は、引数の多いクラスを定義するのが面倒な点です。
こういった場合はどのように実装するのが良いでしょうか。

具体的な失敗
=================

.. code:: python

   class User:
       def __init__(self, username, email, last_name, first_name, birthday, bio, role, mail_confirmed=False):
           self.username = username
           self.email = email
           self.last_name = last_name
           self.first_name = first_name
           self.birthday = birthday
           self.bio = bio
           self.mail_confirmed = mail_confirmed

このプログラムが「問題」というわけではありませんが、冗長な印象があります。

ベストプラクティス
==================

Python3.7から使える :index:`dataclass` を使いましょう。

.. code:: python

   from dataclasses import dataclass
   from datetime import date
   
   
   @dataclass
   class User:
       username: str
       email: str
       last_name: str
       first_name: str
       birthday: date
       role: str
       mail_confirmed: bool = False

``__init__`` メソッドの引数が多いクラスはdataclassを使うと良いでしょう。
各引数の型と :index:`デフォルト引数` を可読性高く設定できます。

.. omission::
