import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_equal_different_text(self):
        node = TextNode("First", TextType.BOLD)
        node2 = TextNode("Second", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_equal_different_type(self):
        node = TextNode("Same text", TextType.BOLD)
        node2 = TextNode("Same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_affects_equality(self):
        # same text and type, but differing url should make them unequal
        node = TextNode("link", TextType.LINK)
        node2 = TextNode("link", TextType.LINK)
        self.assertEqual(node, node2)  # both urls are None by default

        node2.url = "https://example.com"
        self.assertNotEqual(node, node2)

        # if both have the same url they should be equal
        node.url = "https://example.com"
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()