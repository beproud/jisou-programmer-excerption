=====================================
90:KVS（Key Value Store）を利用しよう
=====================================

Webアプリケーションを開発していて「大量のデータをRDBから何度も取得して処理が重くなった」「突然サーバーが高負荷になってしまった」
というような経験はありませんか？


具体的な失敗
==================

たとえばECサイトなどを商品一覧ページなどで、「多数のユーザーがアクセスしにきて重くなるので
表示速度を改善したい」という要望がきたとします。
このとき、RDBから一度取得した商品データをプログラム上でキャッシュして、高速にレスポンスを返すようにしました。

.. code-block:: python

  from app.models import Item
  
  CACHED_ITEMS = None
  
  def items_view(request):
      global CACHED_ITEMS
  
      if CACHED_ITEMS:
          # キャッシュがあるときは RDB(Item) からデータを取得しない
          items = CACHED_ITEMS
      else:
          items = Item.objects.all()
          # すべての商品データをグローバル変数(メモリ)にキャッシュする
          CACHED_ITEMS = list(items)
  
      return render(request, 'items/index.html', {
          "items": items,
      })

ところが、商品データをメモリにすべて載せてしまったために、逆にサーバーのメモリが枯渇してしまい、サイト全体が重くなってしまいました。

ベストプラクティス
==================

プログラムのメモリ上にキャッシュ用のデータを載せずに、:index:`KVS` （Key Value Store）を利用しましょう。

KVSは、MySQL、PostgreSQLのようなRDBとは違い、単純なキーとそれに紐づく値を管理するデータストアです。

.. omission::

