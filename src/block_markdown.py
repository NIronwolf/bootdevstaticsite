import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    splits = markdown.split("\n\n")
    blocks = []
    for split in splits:
        if split != "":
            blocks.append(split.strip())
    return blocks


# ordered_list_counter = 1


def block_to_block_type(block: str) -> BlockType:
    if re.findall(r"^(#{1,6}) ", block):
        return BlockType.HEADING
    if re.findall(r"^```(?:\n[\s\S]*?)?\n```$", block):
        return BlockType.CODE

    lines = block.split("\n")

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children)


def block_to_html_node(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    match block_type:
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case _:
            raise Exception("Unknown block_type")


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block: str) -> HTMLNode:
    parts = re.findall(r"^(#{1,6}) ", block)
    level, text = len(parts[0]), block[len(parts[0]) + 1 :]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block: str) -> HTMLNode:
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def ordered_list_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        "ol",
        [
            ParentNode("li", text_to_children(line.split(". ", 1)[1]))
            for line in block.split("\n")
        ],
    )


def unordered_list_to_html_node(block: str) -> HTMLNode:
    return ParentNode(
        "ul",
        [
            ParentNode("li", text_to_children(line[2:].strip()))
            for line in block.split("\n")
        ],
    )


def quote_to_html_node(block: str) -> HTMLNode:
    lines = block.split("\n")
    quote = " ".join(line[1:].strip() for line in lines)
    return ParentNode("blockquote", text_to_children(quote))
