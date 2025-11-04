import unittest

from utils import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestUtils(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This is plain text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is plain text", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_starts_with_delimiter(self):
        node = TextNode("`code` at start", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_ends_with_delimiter(self):
        node = TextNode("Ends with `code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("Ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_multiple_delimiters(self):
        node = TextNode("`first` and `second` code", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("first", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("second", TextType.CODE),
            TextNode(" code", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_non_text_unchanged(self):
        node1 = TextNode("text", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        node3 = TextNode("text2", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node1, node2, node3], "`", TextType.CODE)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text2", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        expected = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_images_no_images(self):
        matches = extract_markdown_images("This is plain text with no images.")
        self.assertListEqual([], matches)

    def test_extract_markdown_images_empty_alt(self):
        matches = extract_markdown_images("![ ](https://example.com/image.png)")
        self.assertListEqual([(" ", "https://example.com/image.png")], matches)  # Updated to expect the space

    def test_extract_markdown_images_special_chars_in_url(self):
        matches = extract_markdown_images("![alt](https://example.com/path?query=value&other=123)")
        self.assertListEqual([("alt", "https://example.com/path?query=value&other=123")], matches)

    def test_extract_markdown_images_malformed(self):
        matches = extract_markdown_images("This is ![incomplete]( and ![also incomplete")
        self.assertListEqual([], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev")
        ]
        self.assertListEqual(expected, matches)

    def test_extract_markdown_links_no_links(self):
        matches = extract_markdown_links("This is plain text with no links.")
        self.assertListEqual([], matches)

    def test_extract_markdown_links_empty_anchor(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)

    def test_extract_markdown_links_special_chars_in_url(self):
        matches = extract_markdown_links("[link](https://example.com/path?query=value&other=123)")
        self.assertListEqual([("link", "https://example.com/path?query=value&other=123")], matches)

    def test_extract_markdown_links_malformed(self):
        matches = extract_markdown_links("This is [incomplete]( and [also incomplete")
        self.assertListEqual([], matches)

    def test_split_nodes_image_basic(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_image = TextNode("image", TextType.IMAGE)
        expected_image.url = "https://i.imgur.com/zjjcJKZ.png"
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            expected_image,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_multiple(self):
        node = TextNode("![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_image1 = TextNode("rick roll", TextType.IMAGE)
        expected_image1.url = "https://i.imgur.com/aKaOqIh.gif"
        expected_image2 = TextNode("obi wan", TextType.IMAGE)
        expected_image2.url = "https://i.imgur.com/fJRm4Vk.jpeg"
        expected = [
            expected_image1,
            TextNode(" and ", TextType.TEXT),
            expected_image2,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_no_images(self):
        node = TextNode("This is plain text with no images.", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("This is plain text with no images.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_starts_with_image(self):
        node = TextNode("![image](https://example.com/img.png) at start", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_image = TextNode("image", TextType.IMAGE)
        expected_image.url = "https://example.com/img.png"
        expected = [
            expected_image,
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_ends_with_image(self):
        node = TextNode("Ends with ![image](https://example.com/img.png)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected_image = TextNode("image", TextType.IMAGE)
        expected_image.url = "https://example.com/img.png"
        expected = [
            TextNode("Ends with ", TextType.TEXT),
            expected_image,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_non_text_unchanged(self):
        node1 = TextNode("text", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        node3 = TextNode("text2", TextType.TEXT)
        new_nodes = split_nodes_image([node1, node2, node3])
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text2", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_image_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_basic(self):
        node = TextNode("This is text with a [link](https://www.boot.dev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_link = TextNode("link", TextType.LINK)
        expected_link.url = "https://www.boot.dev"
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            expected_link,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_multiple(self):
        node = TextNode("[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_link1 = TextNode("to boot dev", TextType.LINK)
        expected_link1.url = "https://www.boot.dev"
        expected_link2 = TextNode("to youtube", TextType.LINK)
        expected_link2.url = "https://www.youtube.com/@bootdotdev"
        expected = [
            expected_link1,
            TextNode(" and ", TextType.TEXT),
            expected_link2,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is plain text with no links.", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("This is plain text with no links.", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_starts_with_link(self):
        node = TextNode("[link](https://example.com) at start", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_link = TextNode("link", TextType.LINK)
        expected_link.url = "https://example.com"
        expected = [
            expected_link,
            TextNode(" at start", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_ends_with_link(self):
        node = TextNode("Ends with [link](https://example.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected_link = TextNode("link", TextType.LINK)
        expected_link.url = "https://example.com"
        expected = [
            TextNode("Ends with ", TextType.TEXT),
            expected_link,
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_non_text_unchanged(self):
        node1 = TextNode("text", TextType.TEXT)
        node2 = TextNode("bold", TextType.BOLD)
        node3 = TextNode("text2", TextType.TEXT)
        new_nodes = split_nodes_link([node1, node2, node3])
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("text2", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_link_empty_text(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        expected = [TextNode("", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)
        
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        expected_image = TextNode("obi wan image", TextType.IMAGE)
        expected_image.url = "https://i.imgur.com/fJRm4Vk.jpeg"
        expected_link = TextNode("link", TextType.LINK)
        expected_link.url = "https://boot.dev"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            expected_image,
            TextNode(" and a ", TextType.TEXT),
            expected_link,
        ]
        self.assertEqual(nodes, expected)

if __name__ == "__main__":
    unittest.main()