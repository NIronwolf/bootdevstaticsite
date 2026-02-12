import os

from block_markdown import markdown_to_html_node, extract_title


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using template {template_path}"
    )
    with open(from_path, "r") as f:
        markdown = f.read()
        f.close()
    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    with open(template_path, "r") as f:
        template = f.read()
        f.close()
    html = template.replace("{{ Title }}", title).replace(
        "{{ Content }}", html_node.to_html()
    )
    dir = os.path.dirname(dest_path)
    os.makedirs(dir, exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(html)
        f.close()
