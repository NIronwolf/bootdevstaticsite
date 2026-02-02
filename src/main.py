from textnode import TextNode, TextType


def main():
    test = TextNode("This is some acnhor text", TextType.LINK, "https://www.boot.dev")
    print(test)


main()
