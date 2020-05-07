=====================
31:過剰なmockを避ける
=====================

`mock <https://docs.python.org/ja/3/library/unittest.mock.html>`_ は便利なライブラリですが、使いすぎには要注意です。

mockでよくある失敗から、ベストプラクティスを学びましょう。

具体的な失敗
=============

DjangoのView関数をテスト対象として考えます。

.. code:: python

   from .forms import PostSearchForm
   from .posts import search_posts
   
   
   def post_list(request):
       if request.GET:
           form = PostSearchForm(request.GET)
           if form.is_valid():
               text = form.cleaned_data['search']
               posts = search_posts(text)
       else:
           form = PostSearchForm()
           posts = Post.objects.all()
       return TemplateResponse(request, 'post_list.html',
                               {'posts': posts, 'form': form})

このView関数のテストとして :index:`mock` を使いすぎると、次のようになります。

.. code:: python

   from unittest import mock
   from django.test import TestCase
   
   class TestPostList(TestCase):
       @mock.patch('posts.search_posts',
                   return_value=[{'title', 'タイトル', 'body': '本文'}])
       @mock.patch('forms.PostSearchForm')
       def test_search(self, m_search, m_form):
           with mock.patch.object(m_form, 'is_valid', return_value=True):
               res = self.client.get('/posts', data={'search': '本文'})
           
           assert '本文' in res.content.decode()

この例ではView関数の動作のみをテストするためにmockを乱用しています。
しかし、このテストから確認できることは、ほぼありません。
``search=本文`` のように指定されたクエリーパラメーターが正しくフォームで解釈されて、検索に使われて、テンプレートに描画されるつながりを確認できないからです。

ベストプラクティス
=======================

mockを使いすぎるよりも、単純にデータを作成して動作確認をするほうが良いでしょう。

.. code:: python

   class TestPostList(TestCase):
       def test_search(self):
           PostFactory(title='タイトル')
           PostFactory(title='テスト')

           res = self.client.get('/posts', data={'search': 'タイトル'})

           assert "タイトル" in res.content.decode()
           assert "テスト" not in res.content.decode()

.. omission::

関連
====

* :doc:`../ユニットテスト/22-単体テストをする観点から実装の設計を洗練させる`