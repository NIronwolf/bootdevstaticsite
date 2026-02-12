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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(from_path) and entry.endswith(".md"):
            dest_path = dest_path[:-3] + ".html"
            generate_page(from_path, template_path, dest_path)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path)
