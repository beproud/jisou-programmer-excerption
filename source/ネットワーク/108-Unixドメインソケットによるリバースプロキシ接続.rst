==================================================
108:Unixドメインソケットによるリバースプロキシ接続
==================================================

.. column:: 謎のファイル .sock

    * 後輩W：Nginxから ``unix:/var/run/gunicorn.sock`` と指定する手順だったので指定したけれど、 ``No such file or directory`` というエラーが出ました。 ``ls /var/run/`` してみたらファイルがなかったので別の環境から ``gunicorn.sock`` をコピーしてきたけど、動きません。
    * 先輩T：おっと、 ``gunicorn.sock`` はファイルじゃないからコピーで持ってきてもだめだぞ。
    * 後輩W：ファイルじゃない？？
    * 先輩T：たぶん、Gunicornが　``gunicorn.sock`` を用意する構成だと思うけど、Gunicornの起動コマンドオプションはどうなってる？
    * 後輩W：systemdで ``gunicorn -b 0.0.0.0:8000 apps.wsgi:application`` になってます。
    * 先輩T：なるほど、それだとGunicornはTCP 8000で待ち受けしてるのにNginxがUnixドメインソケットでリバースプロキシ接続しようとしてエラーになってるんだね。

.. omission::

ベストプラクティス
==================

WebサーバーとWebアプリケーションサーバーの通信方式を合わせましょう。
可能なら、TCPよりも高速なUnixドメインソケットによるリバースプロキシ接続を使用しましょう。

:index:`Unixドメインソケット` は :index:`ソケット` [#socket]_ の一種で、ネットワーク通信で使います。
ソケットには、Unixドメインソケットの他に、 ``TCP/IP`` や ``UDP`` などがあります。
ソケット通信を行うには、TCP/IP通信であれば ``<IP>:<PORT>`` を使用しますが、Unixドメインソケットによる通信では、ファイルパスを使用します [#unnnamed]_ 。
待ち受け側と接続側の両方でこのファイルパスを使うことで、ソケット通信ができるようになっています。

.. [#socket] https://docs.python.org/ja/3/howto/sockets.html
.. [#unnnamed] 他に、無名ソケットや、抽象名前空間を使ったソケットをバインドできます。詳しくは次のページを参照してください: https://linuxjm.osdn.jp/html/LDP_man-pages/man7/unix.7.html

.. omission::
