import re
from enum import Enum


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
