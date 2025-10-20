print("hello world")
from textnode import TextNode, TextType


def main():
    # create a TextNode with dummy values and print it
    node = TextNode("Example text", TextType.TEXT)
    print(node)
    
if __name__ == "__main__":
    main()
# ...existing code...