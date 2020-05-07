===========================
55:typeカラムを神格化しない
===========================

``type`` というカラムも無思慮に作成されがちです。
少し複雑な仕様の場合に、うまくやろうとして、失敗してしまう場合が多くあります。

具体的な失敗
===================

あるECサイトでは商品に対して「コメント」と「レビュー」が残せるようになっているとします。
コメントとレビューはそれぞれ「投稿者」「タイトル」「本文」があり、レビューには5段階で商品の良し悪しを評価できます。

* ユーザーは投稿する際に「レビュー」にするか「コメント」にするかを選べる
* レビューは集計することで平均の評価数を表示する
* レビューとコメントは1つの画面でまとめて見られるが、別々のものとしても表示できるようにする

この場合、以下のようなモデル設計にしてはいけません。

.. code:: python

   class Comment(models.Model):
       TYPE_COMMENT = 0
       TYPE_REVIEW = 1
       TYPE_CHOICES = (
           (TYPE_COMMENT, "コメント"),
           (TYPE_REVIEW, "レビュー"),
       )
       posted_by = models.ForeignKey(User)
       title = models.CharField(...)
       body = models.TextField(...)
       
       type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES, ...)
       star = models.PositiveSmallInteger(null=True, blank=True)

``type`` によって挙動が大きく変わるのが問題です。
データの内容としては似ているものですが、概念として別のものなので別と扱ったほうが良いです。

.. omission::

ベストプラクティス
==================

単純にテーブルを分けるのが良いでしょう。

.. code:: python

   class Comment(models.Model):
       posted_by = models.ForeignKey(User)
       title = models.CharField(...)
       body = models.TextField(...)
   
   
   class Review(models.Model):
       posted_by = models.ForeignKey(User)
       title = models.CharField(...)
       body = models.TextField(...)
       star = models.PositiveSmallInteger()

.. omission::
