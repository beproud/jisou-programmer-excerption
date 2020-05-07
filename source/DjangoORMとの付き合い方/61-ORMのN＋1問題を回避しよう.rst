============================
61:ORMのN＋1問題を回避しよう
============================

.. maigo:: N＋1問題を回避するORMの書き方は？

    * 後輩W：ログを出して発行されるSQLを確認するのはわかったんですが、件数に比例してSELECTがたくさん発行されてしまうのは、どうやって直せば良いんでしょうか？
    * 先輩T：N＋1問題は、Djangoの場合、 ``select_related`` か ``prefetch_related`` を使えば解決できるよ。
    * 後輩W：それじゃあ、常にそれを使うようにコードを書けば解決するんじゃないですか？
    * 先輩T：いやいや、常に使ってしまうと関連テーブルのデータを全く必要としないときにもデータを取得してデータベースに負荷をかけてしまうことになるよ。

.. index:: N＋1問題
.. index:: Django ORM

具体的な失敗
==================

プログラムのループ処理で、複数のIDそれぞれについてデータベースにSQLを発行すると、件数に比例してクエリ実行回数が増加して、パフォーマンスに影響が出ます。
たとえば以下のようなコードです。

.. code:: python

    def process_tasks(ids):
        for pk in my_ids:
            task = Task.objects.get(pk=id)
            ...

    my_ids = [1, 2, 3, 4, 5]
    process_tasks(my_ids)

このようなコードは、コードレビューなどで指摘されて、すぐに修正されるでしょう。
では、以下のコードではどうでしょうか。

.. code:: python

    def process_tasks(mail: Mail):
        for attach in mail.mailattach_set.all():
            task = attach.task
            ...

    mail = Mail.objects.first()
    process_tasks(mail)

このコードに登場する、mail, attach, taskがどんなオブジェクトなのかは、このコードだけではわかりません。
注意深くレビューする人であれば、変数それぞれが何のオブジェクトなのかを調べることで、問題に気づけるかもしれません。

メールに添付された複数のファイルそれぞれからタスク化して業務を進めるシステムの例を考えてみましょう。

.. omission::

ベストプラクティス
=======================

ログを出力して、発行されているSQLを理解しましょう。
前述の例のように、ログ出力されていれば、どのようなSQLが発行されているかは簡単にわかります。
そのSQLを読み解いて、それがパフォーマンスに影響を及ぼすSQLだと理解する必要があります。

.. index:: prefetch_related

発行されているSQLを読み解いた後は、Django ORMの知識も必要となります。
N＋1問題を回避する方法は、Djangoの公式ドキュメントのQuerySet API reference [#queryset]_ の ``prefetch_related`` に記載されています。

ここでは、 ``prefetch_related`` を使って前述のコードを修正する例を紹介します。

.. [#queryset] https://docs.djangoproject.com/ja/2.2/ref/models/querysets/

.. omission::

関連
====

* :doc:`60-Django_ORMでどんなSQLが発行されているか気にしよう`
* :doc:`../トラブルシューティング・デバッグ/76-シンプルに実装しパフォーマンスを計測して改善しよう`