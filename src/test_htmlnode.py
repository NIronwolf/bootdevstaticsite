import unittest

from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
