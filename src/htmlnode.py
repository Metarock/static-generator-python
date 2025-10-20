class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props is None:
            return ""
        return " " + " ".join(f'{k}="{v}"' for k, v in self.props.items())

    def __repr__(self):
        return f"HTMLNode(tag={self.tag!r}, value={self.value!r}, children={self.children!r}, props={self.props!r})"


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value")
        if self.tag is None:
            return self.value
        props_str = self.props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
    # Its constructor should differ from HTMLNode in that:

    # The tag and children arguments are not optional
    # It doesn't take a value argument
    # props is optional
    # (It's the exact opposite of the LeafNode class)

    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        # If the object doesn't have a tag, raise a ValueError.
        if self.tag is None:
            raise ValueError("ParentNode must have a tag")
        # If children is a missing value, raise a ValueError with a different message.
        if self.children is None:
            raise ValueError("ParentNode must have children")        
        props_str = self.props_to_html()
        children_html = "".join(child.to_html() for child in self.children)
        return f"<{self.tag}{props_str}>{children_html}</{self.tag}>"

def text_node_to_html_node(text_node):
    from textnode import TextType
    if text_node.node_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.node_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.node_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.node_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.node_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.node_type == TextType.IMAGE:
        return LeafNode("img", '', {"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError(f"Unknown TextType: {text_node.node_type}")