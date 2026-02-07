def markdown_to_blocks(markdown: str):
    splits = markdown.split("\n\n")
    blocks = []
    for split in splits:
        if split != "":
            blocks.append(split.strip())
    return blocks
