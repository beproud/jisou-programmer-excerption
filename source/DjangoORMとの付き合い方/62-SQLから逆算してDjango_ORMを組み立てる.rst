========================================
62:SQLから逆算してDjango ORMを組み立てる
========================================

.. index:: Django ORM
.. index:: ORM
.. index:: SQL

.. maigo:: Django ORMで組んだSQLのバグが直らない

    * 先輩T：実装中の、タスク一覧に保留コメントを表示する機能が3日くらい遅れてるけど、問題は解決しそう？
    * 後輩W：はい、一部うまく表示できない問題が解決できました。ただ、ORMで発行されたSQLがテーブルを2重にJOINしていて不安なので動作確認中です。
    * 先輩T：ちょっと気になるね。そういうのを残しておくとパフォーマンス悪化や別のバグの原因になったりするので、確認してみるよ。
    * 後輩W：お願いします。
    * （1時間後）
    * 先輩T：ORM周りのコード、JOINが2重になってるのは直せそうだけど、それ以外にもDBからID数千件を取得してからまたDBに渡したり、コメントに「ORMでNULLを取り除けないのでPythonで除去」って書いてあったりして、だいぶ問題がありそうだね。
    * 後輩W：Django ORMの書き方を変えて試行錯誤したんですけど、1回のクエリ発行では無理そうだったので、わかりやすい方法にしました。
    * 先輩T：いや全然わかりやすくないってｗ ちょっとペアプロで一緒に書き直していこうか。

業務系のWebシステムを開発していると、プログラミングにかける時間の多くは期待するデータを取得するためにデータベースへのクエリをORMで実装する時間に充てられます。
Webシステムがすでに利用中でそこに機能追加を行う場合、すでに実装されているORMのクエリに処理を追加してしまいがちですが、そのような進め方ではなかなか期待どおりの結果は得られないばかりか、パフォーマンス悪化やバグの原因になってしまいます（ :doc:`60-Django_ORMでどんなSQLが発行されているか気にしよう` ）。

具体的な失敗
==================

実例を紹介するため、 :doc:`61-ORMのN＋1問題を回避しよう` で使用したコードを使用します。
3つのDjangoモデル、タスク（Task）、メールの添付ファイル（MailAttach）、メール（Mail）は、それぞれ外部キー参照しています。
タスクには状態 ``state`` があり、添付ファイルがタスク化されると、未処理、処理中、完了、保留、のいずれかの状態を持ち、途中でキャンセルされると ``is_cancelled`` がTrueに設定されます。

ここから、メール一覧画面のためのクエリを実装します。
メール一覧では、タスク化されていない添付ファイルを含むメールを表示します。
そして、2つの機能「保留のみ表示の指定」「保留の場合は保留コメントも表示する」を追加実装したこととします。

以下のコードは、既存のORM実装に試行錯誤してコードを追加した例です。
例示のため、ORMで発行されるSQLをコメントで並記しました。

.. code:: python

    from app.models import *
    from django.db.models import Q

    def get_unprocessed_qs(is_pending_only):
        # まだタスク割当のないMailAttachのIDリストを取得
        # MailAttachから以下の条件に当てはまるものを除外し、振り分けのされていないものの ID のみ取得
        # * タスク割当済み ("保留" 以外の Task と紐付いている)
        # * キャンセルされている ("キャンセル" 状態の Task と紐付いている)
        task_ids = Task.objects.filter(
            ~Q(state=State['保留'])|Q(is_cancelled=True)
        ).values_list('mail_attach', flat=True)
        non_null_ids = filter(None, task_ids)  # NULLを除去
        # 上記条件のタスクに割り当てられていない添付ファイルのIDリストを取得
        non_assigned_mail_attach_ids = MailAttach.objects.exclude(
            id__in=non_null_ids
        ).values_list('pk', flat=True)
        # ここでは以降のSQL例示のため non_assigned_mail_attach_ids == (1, 3, 5) とする

        # タスク割当されていないMailAttachを1つでも持つMailを取得
        qs = Mail.objects.all()
        qs = qs.filter(mailattach__id__in=non_assigned_mail_attach_ids).distinct()

        # ########### タスクを保留にしたユーザ名(Task.changed_by)の一覧を取得

        task_changed_by_names = qs.filter(
            mailattach__task__is_cancelled=False,
            mailattach__task__state=State['保留'],
        ).order_by(
            '-mailattach__task__id'
        ).values_list(
            'pk', 'mailattach__task__changed_by'
        )
        # SELECT DISTINCT mail.id, task.changed_by
        # FROM mail
        #     INNER JOIN mail_attach ON (mail.id = mail_attach.mail_id)
        #     INNER JOIN mail_attach T3 ON (mail.id = T3.mail_id)
        #     INNER JOIN task ON (T3.id = task.mail_attach_id)
        # WHERE (
        #     mail_attach.id IN (
        #         SELECT U0.id FROM mail_attach U0 WHERE NOT (U0.id IN (1, 3, 5)))
        #     AND task.is_cancelled = 0
        #     AND task.state = 4
        # )
        # ORDER BY task.id DESC;

        # qs.filterでtaskのchanged_byがNoneの値をisnullで取り除けないためPythonで除去する
        non_null_task_changed_by_names = [x for x in task_changed_by_names if x[1]]

        # ########### タスク未割当のメール一覧を取得

        if is_pending_only:  # 「保留のみ」指定の場合
            qs = qs.filter(
                mailattach__task__is_cancelled=False,
                mailattach__task__state=State['保留']
            )
            # SELECT DISTINCT mail.id, mail.addr_from, mail.date
            # FROM mail
            #     INNER JOIN mail_attach ON (mail.id = mail_attach.mail_id)
            #     INNER JOIN mail_attach T3 ON (mail.id = T3.mail_id)
            #     INNER JOIN task ON (T3.id = task.mail_attach_id)
            # WHERE (
            #     mail_attach.id IN (
            #         SELECT U0.id FROM mail_attach U0 WHERE NOT (U0.id IN (1, 3, 5)))
            #     AND task.is_cancelled = 0
            #     AND task.state = 4
            # );

        return qs.order_by('date'), non_null_task_changed_by_names

コメント以外のコードは短くシンプルなように見えます。
しかしコードをよく読むと、要件どおりに動作する実装かどうかわかりやすく書けている、とは言えません。

最初にデータベースから取得している ``task_ids`` は、2行後で除外に使うID群ですが、直前のコメントは逆の意味にも読めます。
また ``task_ids`` には保留以外のほぼすべての ``Task.id`` が格納されるため、サービスの運用期間に比例してデータ量が増え、メモリを圧迫し、Webアプリケーションとデータベース間の通信コストが非常に高い状態です。
ORMで発行されるSQLを見ても、 ``mail_attach`` テーブルが2回JOINされていてそれが適切なSQLかどうかすぐにはわかりません。

.. index:: スパゲッティクエリ

.. column:: スパゲッティクエリ

   スパゲッティクエリは、複雑な問題を1つのSQLで解決しようとするアンチパターンです。
   『SQLアンチパターン』（Bill Karwin著、オライリージャパン刊、2013年）で紹介されているアンチパターンの1つで、
   無理に1つのSQLに押し込めようとするあまり、複雑で読み解くことができないSQLを書いてしまう問題を指しています。
   無理に1つのSQLにすることは避けるべきですが、本節の例のようにパフォーマンスに影響が出るような実装もまた避けるべきでしょう。

ベストプラクティス
===========================

**理想のSQL** を書いてから、そのSQLをORMで発行するように実装しましょう。

先ほどの例では、データベースから取得したIDのリストをそのまま次のSQLに渡したり、不要なJOINが行われているという問題がありました。
ソースコメントからも、これが意図した結果ではなくORMをうまく扱えなかった結果だというのが明らかです。
ORMをうまく扱うには、使っているORMライブラリのクセを把握する必要があります。
複雑なクエリを実装するときは先に **理想のSQL** を書いて、そのSQLを使っているORMで再現できるかを検討するのが良いでしょう。

以下のSQLは、要件から期待される理想のSQLです。

.. omission::

関連
======

* :doc:`60-Django_ORMでどんなSQLが発行されているか気にしよう`