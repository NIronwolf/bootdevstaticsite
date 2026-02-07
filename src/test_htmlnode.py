import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_members(self):
        item = HTMLNode("li", "Item 1")
        node = HTMLNode(
            "ul", "My list", [item], {"class": "the-list", "style": "color: red"}
        )
        self.assertEqual(node.tag, "ul")
        self.assertEqual(node.value, "My list")
        self.assertEqual(node.children, [item])
        self.assertEqual(node.props, {"class": "the-list", "style": "color: red"})

    def test_to_html_props(self):
        node = HTMLNode(
            "div", "Hello, world!", None, {"class": "my-class", "id": "my-id"}
        )
        self.assertEqual(node.props_to_html(), ' class="my-class" id="my-id"')

    def test_defaults(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_repr(self):
        child = HTMLNode("span", "Child text")
        node = HTMLNode("a", "Click Here!", [child], {"href": "https://boot.dev"})
        expected_repr = "HTMLNode(a, Click Here!, children: [HTMLNode(span, Child text, children: None, None)], {'href': 'https://boot.dev'})"
        self.assertEqual(repr(node), expected_repr)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Here!", {"href": "https://boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">Click Here!</a>')

    def test_parent_to_html_with_children(self):
        child1 = LeafNode("li", "Item 1")
        child2 = LeafNode("li", "Item 2")
        node = ParentNode("ul", [child1, child2], {"class": "my-list"})
        expected_html = '<ul class="my-list"><li>Item 1</li><li>Item 2</li></ul>'
        self.assertEqual(node.to_html(), expected_html)

    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<h2><b>Bold text</b>Normal text<i>italic text</i>Normal text</h2>",
        )

    def test_parent_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_missing_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_missing_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
