===========================
82:Docker公式のPythonを使う
===========================

Docker公式のPythonを利用するメリット、デメリットは以下のとおりです。

* ○ Pythonの好きなバージョンを選べる（2016年以降のすべてのバージョンが提供されている）
* △ セキュリティー更新の確認は各自で行う
* △ 更新の適用と互換性の確認コストが低～中程度。コンテナの入れ替え、差分の影響確認が必要

ベストプラクティス
===========================

.. index:: Docker

Docker公式のPythonを使って、運用コストを下げつつ、セキュリティー更新していきましょう。
Docker公式のDockerHub [#dockerhub]_ にPythonのDocker Imageがあります。

.. [#dockerhub] https://hub.docker.com/_/python

.. omission::

