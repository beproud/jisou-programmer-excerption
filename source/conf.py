import os
import sys
sys.path.insert(0, os.path.abspath('./ext'))

project = '自走プログラマー【抜粋版】'
copyright = '2020, BeProud Inc.'
author = ' 清原 弘貴、清水川 貴之、tell-k、株式会社ビープラウド（監修）'

extensions = [
    'sphinx.ext.todo',
    'support',
]
todo_include_todos = False
templates_path = ['_templates']
language = 'ja'
show_authors = False
numfig = True
exclude_patterns = []

rst_prolog = """
.. |cover| image:: /_static/cover.jpg
   :target: https://gihyo.jp/book/2020/978-4-297-11197-7
"""


html_theme = 'bizstyle'
html_static_path = ['_static']
html_sidebars = {
    # add 'pageinfo.html' to display the panel.
    '**': ['bookbanner.html', 'localtoc.html', 'relations.html', 'sourcelink.html', 'searchbox.html']
}


latex_documents = [
    ('index', 'archbook.tex', project, author, 'manual', True),
]
latex_elements = {
    'papersize': 'b5paper',
    'figure_align': 'H',
    'preamble': r'''
      \geometry{top=1.5cm, bottom=1cm, left=1cm, right=1cm, includefoot}
      \usepackage{titlesec}
      \titleclass{\chapter}{top}
      \titleformat{\chapter}
        [display]  % shape
        {\centering\normalfont\huge\bfseries} % format
        {\titlerule[5pt]\vspace{3pt}\titlerule[2pt]\vspace{1em}\chaptertitlename \thechapter 章} % laberl
        {0pt} % sep
        {\vspace{3pt}\Huge} % before-code
        % code
        [{\vspace{1em}\titlerule[2pt]\vspace{3pt}\titlerule[5pt]}] % after-code

      \titleformat{\section}[block]
        {\normalfont\huge\bfseries} % format
        {\clearpage\titlerule[2pt]\vspace{2pt}\thesection.} % label
        {0.5em} % sep
        {\vspace{3pt}\huge} % before-code
        [{\vspace{2pt}\titlerule[2pt]}] % after-code
        
      \setcounter{secnumdepth}{2}
      \setcounter{tocdepth}{2}
      
      \usepackage{hyperref}
      \usepackage{pxjahyper}

      \hypersetup{bookmarksnumbered}
    '''
}
latex_show_urls = 'footnote'
latex_use_xindy = True
latex_show_pagerefs = True
