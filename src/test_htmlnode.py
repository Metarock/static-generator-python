import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_no_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_with_props(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_single_prop(self):
        node = HTMLNode(props={"class": "my-class"})
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_to_html_basic(self):
        child = LeafNode("b", "bold text")
        parent = ParentNode("p", [child])
        self.assertEqual(parent.to_html(), "<p><b>bold text</b></p>")

    def test_parent_to_html_multiple_children(self):
        child1 = LeafNode("b", "bold")
        child2 = LeafNode(None, " normal ")
        child3 = LeafNode("i", "italic")
        parent = ParentNode("p", [child1, child2, child3])
        self.assertEqual(parent.to_html(), "<p><b>bold</b> normal <i>italic</i></p>")

    def test_parent_to_html_nested(self):
        grandchild = LeafNode("b", "bold")
        child = ParentNode("span", [grandchild])
        parent = ParentNode("div", [child])
        self.assertEqual(parent.to_html(), "<div><span><b>bold</b></span></div>")

    def test_parent_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "container"})
        self.assertEqual(parent.to_html(), '<div class="container"><span>child</span></div>')

    def test_parent_to_html_empty_children(self):
        parent = ParentNode("p", [])
        self.assertEqual(parent.to_html(), "<p></p>")

    def test_parent_to_html_no_tag(self):
        parent = ParentNode(None, [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parent_to_html_no_children(self):
        parent = ParentNode("p", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("Bold text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Bold text")

    def test_italic(self):
        node = TextNode("Italic text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Italic text")

    def test_code(self):
        node = TextNode("Code text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Code text")

    def test_link(self):
        node = TextNode("Link text", TextType.LINK)
        node.url = "https://example.com"
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Link text")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE)
        node.url = "https://example.com/image.jpg"
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com/image.jpg", "alt": "Alt text"})


if __name__ == "__main__":
    unittest.main()