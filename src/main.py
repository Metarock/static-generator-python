import sys
from textnode import TextNode, TextType
from helpers import copy_static_to_public
from utils import  generate_pages_recursive

def main():
    # use sys.argv to garb first cli argument to program, save it as
    # basepath. if one isnt provided default to /
    if (len(sys.argv) > 1):
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    # call the function to copy static to public
    copy_static_to_public(public_dir='docs')
    # template.html is in root project
    # pass basepath 
    generate_pages_recursive("content", "template.html", "docs", basepath)
    
if __name__ == "__main__":
    main()
# ...existing code...