import re

from enum import Enum
from htmlnode import ParentNode, text_node_to_html_node, LeafNode
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

class BlockNode:
    def __init__(self, content):
        self.content = content
        self.children = []
    
    # put markdown_to_blocks
    def markdown_to_blocks(markdown):
        blocks = []
        current_block = []
        lines = markdown.split("\n")
        
        # loop through the lines
        # we also want to remove any "empty" blocks due to excessive lines
        for line in lines:
            # we want to strip any leading or trailing whitespace
            stripped_line = line.strip()
            if stripped_line == "":
                # if we hit an empty line, we finalize the current block
                if current_block:
                    blocks.append("\n".join(current_block).strip())
                    current_block = []
            else:
                current_block.append(stripped_line)

        # add the last block if exists
        if current_block:
            blocks.append("\n".join(current_block).strip())

        return blocks
    
    # takes a single block of markdown text as input and returns the BlockType representing its type.
    # assume all leading and trailing whitespace has been removed.
    def block_to_block_type(block):
        lines = block.split("\n")

        if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
            return BlockType.HEADING
        if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
            return BlockType.CODE
        if block.startswith(">"):
            for line in lines:
                if not line.startswith(">"):
                    return BlockType.PARAGRAPH
            return BlockType.QUOTE
        if block.startswith("- "):
            for line in lines:
                if not line.startswith("- "):
                    return BlockType.PARAGRAPH
            return BlockType.UNORDERED_LIST
        if block.startswith("1. "):
            i = 1
            for line in lines:
                if not line.startswith(f"{i}. "):
                    return BlockType.PARAGRAPH
                i += 1
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH