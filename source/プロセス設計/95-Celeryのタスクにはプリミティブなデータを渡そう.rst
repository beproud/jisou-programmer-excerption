=================================================
95:Celeryのタスクにはプリミティブなデータを渡そう
=================================================

:index:`Celery` のようなジョブキューシステムを利用するとき、ジョブに渡すデータが大きいと、
思わぬ不具合に遭遇します。ここでは、なるべく不具合になりにくいデータの渡し方についてご紹介します。


具体的な失敗例
==================

下記のコードはDjangoのProductItemというモデルのデータを
オブジェクトそのままにCeleryのタスクに渡しているコードです。


.. code:: python

   # Celeryのタスク
   @shared_task
   def update_items_task(items, new_attr):
       for item in items:
          if item.attr != new_attr:
             item.attr = new_attr
             item.save()
             

   # タスクの呼び出し元
   def some_process(product_item_ids, new_attr):
       target_items = ProductItem.objects.filter(id__in=product_item_ids)
       update_items_task.delay(target_items, new_attr)


コードとしてはシンプルですが、DjangoからCeleryへの通信コストという点では、
複雑なデータ構造を持つPythonのオブジェクトはあまり良くありません。

.. omission::

ベストプラクティス
=========================

Celeryのような専用のデーモンを立ち上げて処理するようなシステムにデータを送るときは、なるべくプリミティブ（原始的）なデータにしましょう。
たとえば ``int`` や ``str`` などのシンプルな値です。受け取った側ではでプリミティブなデータから、本当に必要なデータを取り出して利用しましょう。

.. code:: python

   @shared_task
   def update_items_task(item_ids, new_attr):
       for item in ProductItem.objects.filter(id__in=item_ids): # <- 受け取ったIDから必要なデータを取得する
          if item.attr != new_attr:
             item.attr = new_attr
             item.save()

   def some_process(product_item_ids, new_attr):
       target_items = ProductItem.objects.filter(id__in=product_item_ids)
       update_items_task.delay([t.id for t in target_items], new_attr) # <- id(int)のリストだけを渡す


ここでは ``id`` のリストだけをCeleryに渡し、受け取ったタスク側で ``id`` を元に最新のモデル情報を取得しています。
こうすることで、送信するデータ量を抑えつつ、常に最新の状態でタスクを処理できます。