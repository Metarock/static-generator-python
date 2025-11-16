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
    def block_to_block_type(markdown):
        # headings start with 1-6 # followed by a space and heading text
        if re.match(r'^(#{1,6})\s', markdown):
            return BlockType.HEADING
        # codeblocks must start with 3 backticks and end with 3 backticks.
        if re.match(r'^```', markdown) and re.search(r'```$', markdown):
            return BlockType.CODE
        # every line in a quote block start with >
        if all(re.match(r'^>\s', line) for line in markdown.split("\n")):
            return BlockType.QUOTE
        
        # every line an unordered list block must start with a - character, followed by a space
        if all(re.match(r'^-\s', line) for line in markdown.split("\n")):
            return BlockType.UNORDERED_LIST

        # every line in an ordered list block must start with a number followed by a period and a space
        if all(re.match(r'^\d+\.\s', line) for line in markdown.split("\n")):
            return BlockType.ORDERED_LIST

        return BlockType.PARAGRAPH