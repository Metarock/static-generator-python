import unittest

from blocknode import BlockNode


class TestUtils(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
                This is **bolded** paragraph

                This is another paragraph with _italic_ text and `code` here
                This is the same paragraph on a new line

                - This is a list
                - with items
                """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_paragraph(self):
        md = "This is a single paragraph."
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single paragraph."])

    def test_markdown_to_blocks_multiple_paragraphs(self):
        md = """
        First paragraph.

        Second paragraph.

        Third paragraph.
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["First paragraph.", "Second paragraph.", "Third paragraph."])

    def test_markdown_to_blocks_with_headings(self):
        md = """
        # Heading 1

        Some text under heading.

        ## Heading 2

        More text.
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Heading 1", "Some text under heading.", "## Heading 2", "More text."])

    def test_markdown_to_blocks_with_lists(self):
        md = """
        - Item 1
        - Item 2

        1. Ordered item 1
        2. Ordered item 2
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["- Item 1\n- Item 2", "1. Ordered item 1\n2. Ordered item 2"])

    def test_markdown_to_blocks_with_code_block(self):
        md = """
        ```
        code block
        ```

        Normal text.
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["```\ncode block\n```", "Normal text."])

    def test_markdown_to_blocks_empty_markdown(self):
        md = ""
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_only_empty_lines(self):
        md = "\n\n\n"
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_markdown_to_blocks_leading_trailing_whitespace(self):
        md = """
           Paragraph with leading spaces.

        Another paragraph.
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["Paragraph with leading spaces.", "Another paragraph."])

    def test_markdown_to_blocks_mixed_content(self):
        md = """
        # Title

        Some paragraph text.

        - List item 1
        - List item 2

        ```
        code
        ```
        """
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["# Title", "Some paragraph text.", "- List item 1\n- List item 2", "```\ncode\n```"])

    def test_markdown_to_blocks_no_empty_lines(self):
        md = "Line 1\nLine 2\nLine 3"
        blocks = BlockNode.markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1\nLine 2\nLine 3"])

if __name__ == "__main__":
    unittest.main()