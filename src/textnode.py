from enum import Enum

# text enum node types
class TextType(Enum):
    TEXT = 'text'
    BOLD = 'bold'
    ITALIC = 'italic'
    CODE = 'code'
    LINK = 'link'
    IMAGE = 'image'
    

class TextNode:
    def __init__(self, text: str, node_type: TextType):
        self.text = text
        self.node_type = node_type
        self.url = None  # for LINK and IMAGE types
    
    def __eq__(self, value):
        # i all of the properties of two TextNode objects are equal. Our future unit tests will rely on this method to compare objects.
        if not isinstance(value, TextNode):
            return False
        return (self.text == value.text and
                self.node_type == value.node_type and
                self.url == value.url)  
    
    def __repr__(self):
        # returns a string representation of the TextNode object. It should look like this:
        return f'TextNode(text="{self.text}", node_type={self.node_type}, url="{self.url}")'