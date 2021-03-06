=======================
49:NULLをなるべく避ける
=======================

テーブル定義で最も重要になることは、いかに「制約をつけるか」ということです。
次のような、「寛容な」設計にしていませんか？

この節では、テーブル定義についてはDjangoのモデルで説明します。

具体的な失敗
====================

.. code:: python

   class Product(models.Model):
       name = models.CharField("商品名", max_length=255, null=True, blank=True)
       
       @property
       def name_display(self):
           if not self.name:
               return "<商品名なし>"
           return name

この商品（Product）モデルは商品名がないデータを許容しています。
ですが本当に「商品名がない商品」を受け入れる必要があるのでしょうか？

ベストプラクティス
==================

テーブルのカラムをなるべく :index:`NULL可能` にしないようにします。
NULL可能にする前に、本当に必要か、他の方法で解決できないかを立ち止まって考えることが大切です。

商品名であれば単に「NULLにはできない」という仕様にします。

.. code:: python

   class Product(models.Model):
       name = models.CharField("商品名", max_length=255)

``NULL`` を許容するとアプリケーション側で「NULLの場合」を扱う必要が出ます。
NULLを扱う処理や仕様が必要になり、プログラムが煩雑になります。制約が少なくなるとアプリケーションで想定するケースが増えるのが問題です。
今回の失敗では「 ``Product.name`` がNULL（None）のとき」を扱う必要があります。特に「商品名がない商品」という仕様が求められないのであれば、NULL不可が良いです。
「不用意な親切心」で甘い制約のテーブル設計にしないようにしましょう。

とはいえ「何でもNULL不可にはできない」という場合もあります。
デフォルト値を使ったNULL可能の回避方法を紹介します。

.. omission::

