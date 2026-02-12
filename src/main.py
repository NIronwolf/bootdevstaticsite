from copystatic import init_public
from gencontent import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"


def main():
    init_public(dir_path_static, dir_path_public)

    print("Generating pages...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public)


main()
