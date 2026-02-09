import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


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


if __name__ == "__main__":
    unittest.main()
