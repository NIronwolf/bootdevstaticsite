import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_simple_text(self):
        node = TextNode("This is a simple text node", TextType.TEXT)
        test_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(test_nodes, [node])

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        test_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(test_nodes, expected_nodes)

    def test_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        test_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(test_nodes, expected_nodes)

    def test_unmatched_delimiter(self):
        node = TextNode("This is **bold text with unmatched delimiter", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(context.exception), 'Unmatched delimiter "**" in text')

    def test_multiple_delimiters(self):
        node = TextNode("This is **bold** and `code` text", TextType.TEXT)
        test_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        test_nodes = split_nodes_delimiter(test_nodes, "`", TextType.CODE)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(test_nodes, expected_nodes)

    def test_italic_text(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        test_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected_nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(test_nodes, expected_nodes)
