# -*- coding: utf-8 -*-

from docutils.parsers.rst.directives.admonitions import Admonition
from sphinx.directives import SphinxDirective
from docutils import nodes, statemachine
from sphinx.locale import _


class ColumnDirective(Admonition):
    node_class = nodes.admonition
    required_arguments = 1
    title_prefix = 'コラム:　'

    def run(self):
        self.arguments[0] = self.title_prefix + self.arguments[0]
        self.options.setdefault('class', []).append(self.name)
        r = Admonition.run(self)
        r[0]['name'] = self.name
        return r


class MaigoDirective(ColumnDirective):
    title_prefix = 'プログラミング迷子: '


class OmissionDirective(SphinxDirective):
    name = 'omission'

    def run(self):
        self.content = statemachine.StringList([
            '|cover|',
            '',
            '（中略）詳細は書籍 `自走プログラマー <https://gihyo.jp/book/2020/978-4-297-11197-7>`__ をご参照ください',
        ])
        text = '\n'.join(self.content)
        admonition_node = nodes.admonition(text, **{'classes': [self.name]})
        self.add_name(admonition_node)
        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]


from sphinx import addnodes
from sphinx.util.nodes import process_index_entry


class IndexRole(object):

    def __init__(self, node_class):
        self.node_class = node_class

    def __call__(self, name, rawtext, text, lineno, inliner, options={}, content=[]):
        targetnode = nodes.target('', '')
        inliner.document.note_explicit_target(targetnode)
        targetid = targetnode['ids'][0]
        indexnode = addnodes.index()
        indexnode['entries'] = ne = []
        indexnode['inline'] = True
        indexnode.source, indexnode.line = inliner.document.current_source, lineno
        ne.extend(process_index_entry(text, targetid))
        textnode = self.node_class(text, text)
        return ([textnode, indexnode, targetnode], [])


from docutils.transforms import Transform


class IdxTransform(Transform):
    """
    Replace emphasis node in any title/caption node.
    """
    # run before the cross reference
    default_priority = 210

    def apply(self):
        def is_title_node(n):
            return isinstance(n, (nodes.title, nodes.caption))

        for title_node in self.document.traverse(is_title_node):
            for c in title_node.traverse(nodes.emphasis):
                c.replace_self(c.children)


class PepTransform(Transform):
    """
    Remove strong node for pep role.
    """
    # run before the cross reference
    default_priority = 210

    def apply(self):
        def is_pep_strong(n):
            return (
                isinstance(n, nodes.strong) and
                isinstance(n.parent, nodes.reference) and
                'pep' in n.parent['classes']
            )

        for node in self.document.traverse(is_pep_strong):
            node.replace_self(node.children)


def setup(app):
    app.add_role('idx', IndexRole(nodes.emphasis))
    app.add_role('idx2', IndexRole(nodes.literal))
    app.add_transform(IdxTransform)
    app.add_transform(PepTransform)
    app.add_directive('column', ColumnDirective)
    app.add_directive('maigo', MaigoDirective)
    app.add_directive('omission', OmissionDirective)
    app.add_css_file('custom.css')
