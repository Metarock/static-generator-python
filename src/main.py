print("hello world")
from textnode import TextNode, TextType
from helpers import copy_static_to_public
from utils import generate_page

def main():
    # create a TextNode with dummy values and print it
    node = TextNode("Example text", TextType.TEXT)
    # COMMENT OUT FOR NOW
    # print(node)
    # call the function to copy static to public
    copy_static_to_public()
    # template.html is in root project
    generate_page("content/index.md", "template.html", "public/index.html")
    
if __name__ == "__main__":
    main()
# ...existing code...