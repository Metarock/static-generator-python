import unittest

from blocknode import BlockNode, BlockType


class TestBlockNode(unittest.TestCase):
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

    def test_block_to_block_type_heading(self):
        self.assertEqual(BlockNode.block_to_block_type("# Heading"), BlockType.HEADING)
        self.assertEqual(BlockNode.block_to_block_type("## Subheading"), BlockType.HEADING)
        self.assertEqual(BlockNode.block_to_block_type("###### Level 6"), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        self.assertEqual(BlockNode.block_to_block_type("```\ncode\n```"), BlockType.CODE)
        self.assertEqual(BlockNode.block_to_block_type("```\nline1\nline2\n```"), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        self.assertEqual(BlockNode.block_to_block_type("> Quote line"), BlockType.QUOTE)
        self.assertEqual(BlockNode.block_to_block_type("> Line 1\n> Line 2"), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        self.assertEqual(BlockNode.block_to_block_type("- Item 1"), BlockType.UNORDERED_LIST)
        self.assertEqual(BlockNode.block_to_block_type("- Item 1\n- Item 2"), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        self.assertEqual(BlockNode.block_to_block_type("1. Item 1"), BlockType.ORDERED_LIST)
        self.assertEqual(BlockNode.block_to_block_type("1. Item 1\n2. Item 2"), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        self.assertEqual(BlockNode.block_to_block_type("This is a paragraph."), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("Line 1\nLine 2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_heading(self):
        self.assertEqual(BlockNode.block_to_block_type("#No space"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("####### Too many"), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_code(self):
        self.assertEqual(BlockNode.block_to_block_type("```no end"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("no start```"), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_quote(self):
        self.assertEqual(BlockNode.block_to_block_type(">Missing space"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("> Line 1\nLine 2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_unordered_list(self):
        self.assertEqual(BlockNode.block_to_block_type("-No space"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("- Item 1\nItem 2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_invalid_ordered_list(self):
        self.assertEqual(BlockNode.block_to_block_type("1.No space"), BlockType.PARAGRAPH)
        self.assertEqual(BlockNode.block_to_block_type("1. Item 1\n2 Item 2"), BlockType.PARAGRAPH)

    def test_block_to_block_type_empty_block(self):
        self.assertEqual(BlockNode.block_to_block_type(""), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()