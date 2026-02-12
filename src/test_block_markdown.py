import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html_node,
    extract_title,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type(self):
        blocks = [
            "# Heading 1",
            "## Heading 2",
            "### Heading 3",
            "#### Heading 4",
            "##### Heading 5",
            "###### Heading 6",
            "This is a paragraph.",
            "> This is a quote.",
            "- This is an unordered list item.",
            "1. This is an ordered list item.",
        ]
        self.assertEqual(block_to_block_type(blocks[0]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[1]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[2]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[3]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[4]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[5]), BlockType.HEADING)
        self.assertEqual(block_to_block_type(blocks[6]), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(blocks[7]), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(blocks[8]), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(blocks[9]), BlockType.ORDERED_LIST)
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "1. list\n- not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "- list\n1. not a list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = "> quote\nnot a quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        block = '```json\n{\n  "key": "value"\n}\n```'  # code type not supported
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        # ordered list must start at 1
        block = "2. not starting at one\n3. still ordered"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

        # ordered list must not skip numbers
        block = "1. first\n3. skipped two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = """
# Heading 1

## Heading 2

### Heading 3

#### Heading 4

##### Heading 5

###### Heading 6

# Heading 1 with **bold** and _italic_ text
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h2>Heading 2</h2><h3>Heading 3</h3><h4>Heading 4</h4><h5>Heading 5</h5><h6>Heading 6</h6><h1>Heading 1 with <b>bold</b> and <i>italic</i> text</h1></div>",
        )

    def test_quote(self):
        md = """
> This is a quote

> This is a quote with **bold** and _italic_ text

> This is a
> multiline quote
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote</blockquote><blockquote>This is a quote with <b>bold</b> and <i>italic</i> text</blockquote><blockquote>This is a multiline quote</blockquote></div>",
        )

    def test_unordered_list(self):
        md = """
- list item 1
- list item 2 with **fancy** _text_

- another list
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>list item 1</li><li>list item 2 with <b>fancy</b> <i>text</i></li></ul><ul><li>another list</li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. ordered list

1. Item 1
2. Item 2 has `code`!
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>ordered list</li></ol><ol><li>Item 1</li><li>Item 2 has <code>code</code>!</li></ol></div>",
        )

    def test_paragraphs2(self):
        md = """
This is just a
paragraph.

This is another paragraph
but with some **bold** and
_italic_ and `code` text in it.
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is just a paragraph.</p><p>This is another paragraph but with some <b>bold</b> and <i>italic</i> and <code>code</code> text in it.</p></div>",
        )


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        actual = extract_title("# This is a title")
        self.assertEqual(actual, "This is a title")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")

    def test_none(self):
        try:
            extract_title(
                """
no title
"""
            )
            self.fail("Should have raised an exception")
        except Exception as e:
            pass


if __name__ == "__main__":
    unittest.main()
