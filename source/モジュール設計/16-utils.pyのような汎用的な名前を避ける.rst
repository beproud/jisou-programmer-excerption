=======================================
16:utils.pyのような汎用的な名前を避ける
=======================================

Pythonのモジュール（Pythonファイル）を分割するとき、とりあえずで ``utils.py`` という名前にしていませんか？

具体的な失敗
===================

以下のような関数をすべて ``utils.py`` にまとめるのはやめましょう。

.. code-block:: python
   :caption: utils.py

   from datetime import timedelta
   from urllib.parse import urlencode
   
   from payment.models import Purchase

   
   def get_purchase(purchase_id):
       return Purchase.objects.filter(published_at__isnull=False).get(id=purchase_id)
   
   
   def takeover_query(get_params, names):
       return urlencode({k: v for k, v in get_params.items() if k in names})
   
   
   def date_range(start, end, step=1):
       current = start
       while current <= end:
           yield current
           current += timedelta(days=step)

``utils.py`` というモジュール名はなるべく使わないのが良いでしょう。
ビジネス上の仕様に深く関わる処理や、データの仕様などに関係する処理を、「ユーティリティ」というモジュールにまとめるのは不適切です。
ユーティリティには「有益なもの」「便利なもの」くらいのニュアンスしかありません。

ベストプラクティス
========================

まずデータをフィルターする処理は ``models.py`` などにまとめるのが良いです。
Djangoフレームワークを使う場合はQuerySetのメソッドに実装できます。

.. code-block:: python
   :caption: models.py

   from django.db import models
   
   
   class PurchaseQuerySet(models.QuerySet):
       def filter_published(self):
           return self.filter(published_at__isnull=False)
   
   
   class Purchase(models.Model):
       ...
       objects = PurchaseQuerySet.as_manager()

また、「リクエスト」に関係する処理であれば、 ``request.py`` など別のモジュールを作るのが良いでしょう。

.. omission::

関連
====

* :doc:`17-ビジネスロジックをモジュールに分割する`