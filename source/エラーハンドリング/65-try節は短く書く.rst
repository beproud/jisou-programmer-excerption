==================
65:try節は短く書く
==================

.. maigo:: 大きいtry節は小さいtry節を兼ねる？

    * 先輩T：今朝言ってたバグの調査、けっこう手間取ってる？
    * 後輩W：すいません、どこで問題が出てるかまだわからなくて……。
    * 先輩T：どれどれ……うわ、try節長いなー。これだとどこでバグってるかわからなそうだ。
    * 後輩W：tryって長いとだめなんですか？
    * 先輩T：そうだねー、できるだけ短いほうがいいね。

例外の処理を書き慣れていないと、とても長い :index:`try節` を書いてしまいます。
このとき、1つの :index:`except節` ですべてのエラー処理をまとめてしまうと、どの行でどんなエラーが起きたかわからなくなってしまいます。

具体的な失敗
===============

たとえば、以下のようなWebアプリケーションのフォームを処理するコードがあるとします。
このコードは、エラーが発生した際に問題を切り分けられないというバグを含んでいます。

.. code:: python

    def purchase_form_view(request):
        try:
            product = get_product_by_id(int(request.POST['product_id']))
            purchase_count = request.POST['purchase_count']
            if purchase_count <= product.stock.count:
                product.stock.count -= int(request.POST['purchase_count'])
                product.stock.save()
                return render(request, 'purchase/result.html', {
                    'purchase': create_purchase(
                        product=product,
                        count=int(purchase_count),
                        amount_price=purchase_count * product.price,
                    )
                })
        except:
            return render(request, 'error.html')  # エラーが発生しました、と表示

このコードは、関数内のすべての処理をtry節に書き、 except節ですべての例外を捕まえて、エラー処理をしています。
ここで、Webアプリケーションの利用中に例外が発生しても、画面には「エラーが発生しました」とだけ表示されるため、ユーザーにも開発者にもエラーの原因はわかりません。
エラーの原因の可能性として、ユーザーからのパラメータが想定外、他の処理でDBに保存したデータに問題がある、実装に変数名間違いなど単純なバグがある、ライブラリの更新で動作が変わった……など、多くの可能性があります。このため、開発者が原因を調べて不具合を解消するのにとても時間がかかってしまいます。


ベストプラクティス
==================

try節のコードはできるだけ短く、1つの目的に絞って処理を実装しましょう。

try節に複数の処理を書いてしまうと、発生する例外の種類も比例して多くなっていき、except節でいろいろな例外処理が必要になってしまいます。
次のコードは、try節の目的を絞ってそれぞれ個別の例外処理を行うことで、わかりやすいエラーメッセージをユーザーに伝えています。
これによって、ユーザーが正しい状態に復帰できるようにしています。

.. omission::

