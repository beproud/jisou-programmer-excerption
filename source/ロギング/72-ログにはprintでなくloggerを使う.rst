==================================
72:ログにはprintでなくloggerを使う
==================================

とりあえずで ``print`` を仕込んでデバッグしていませんか？　
Pythonのロギングの仕組みを使ってより良い書き方を学びましょう。

具体的な失敗
=================

.. code:: python

   def main():
       print("売上CSV取り込み処理を開始")
       sales_data = load_sales_csv():
       print(f"{len(sales_data)}件のデータを処理します")

printでのデバッグやprintでの実行ログも悪くはありません。
ですが、環境によって切り替えができない点が不便です。

ベストプラクティス
=====================

ロギングを使うことで、より便利になります。

.. code:: python

   def main():
       logger.info("売上CSV取り込み処理を開始")
       sales_data = load_sales_csv():
       logger.info("%s件のデータを処理します", len(sales_data))
       ...

ロギングを使えば、表示をやめたり、ファイルに出力したり、ログを残した日時を残したりできます。

.. omission::
