import sys
from textnode import TextNode, TextType
from helpers import copy_static_to_public
from utils import  generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    # use sys.argv to garb first cli argument to program, save it as
    # basepath. if one isnt provided default to /
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    
    # call the function to copy static to public
    copy_static_to_public(dir_path_static, dir_path_public)
    # template.html is in root project
    # pass basepath 
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)
    
if __name__ == "__main__":
    main()
# ...existing code...