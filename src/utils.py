import re

from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from blocknode import BlockNode, BlockType

    

def extract_title(markdown):
    # It should pull the h1 header from the markdown file (the line that starts with a single #) and return it.
    #If there is no h1 header, raise an exception.
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []
    
    for node in old_nodes:
            # leave non-text nodes unchanged
            if node.node_type != TextType.TEXT:
                new_nodes.append(node)
            else:
                # spit the text node by the delimiter
                parts = node.text.split(delimiter)
                
                # alternate between TEXT and specified text_type
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(part, text_type))
    return new_nodes
                

# extract 
# takes in raw markdown text and returns a list of tuples. 
#  each tuple contains the alt text and URL of an image found in the markdown.
# text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
# print(extract_markdown_images(text))
# # [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

# create a similar function for links
def extract_markdown_links(text):
    pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches



# will behave similar to split_nodes_delimiter but for images
def split_nodes_image(old_nodes):
    
    new_nodes = []
    
    for node in old_nodes:
         if node.node_type != TextType.TEXT:
                new_nodes.append(node)
         else:
                # extract markdown images from the text
                matches = extract_markdown_images(node.text)
                
                if not matches:
                    new_nodes.append(node)
                else:
                    # split the text by the image markdown
                    parts = re.split(r'!\[[^\]]*\]\([^)]+\)', node.text)
                    
                    for i in range(len(parts)):
                        # add the text part
                        if parts[i]:
                            new_nodes.append(TextNode(parts[i], TextType.TEXT))
                        
                        # add the image part if exists
                        if i < len(matches):
                            alt_text, url = matches[i]
                            image_node = TextNode(alt_text, TextType.IMAGE)
                            image_node.url = url
                            new_nodes.append(image_node)
    return new_nodes
    
    
    
def split_nodes_link(old_nodes):
    
    new_nodes = []
    
    for node in old_nodes:
         if node.node_type != TextType.TEXT:
                new_nodes.append(node)
         else:
                # extract markdown links from the text
                matches = extract_markdown_links(node.text)
                
                if not matches:
                    new_nodes.append(node)
                else:
                    # split the text by the link markdown
                    parts = re.split(r'\[[^\]]*\]\([^)]+\)', node.text)
                    
                    for i in range(len(parts)):
                        # add the text part
                        if parts[i]:
                            new_nodes.append(TextNode(parts[i], TextType.TEXT))
                        
                        # add the link part if exists
                        if i < len(matches):
                            link_text, url = matches[i]
                            link_node = TextNode(link_text, TextType.LINK)
                            link_node.url = url
                            new_nodes.append(link_node)
    return new_nodes


def text_to_textnodes(text):
    # Start with a single TEXT node
    nodes = [TextNode(text, TextType.TEXT)]
    # Split for bold
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    # Split for italic
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    # Split for code
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # Split for images
    nodes = split_nodes_image(nodes)
    # Split for links
    nodes = split_nodes_link(nodes)
    return nodes

def block_to_html_heading(block):
        level = 0
        for char in block:
            if char == '#':
                level += 1
            else:
                break
        # only up to heading 6
        if level > 6:
            level = 6
        tag = f'h{level}'
        content = block[level:].strip()
        text_nodes = text_to_textnodes(content)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        return ParentNode(tag, html_nodes)


def block_to_html_code(block):
    content = block.strip('```').strip()
    return ParentNode("pre", [LeafNode("code", content)])

def block_to_html_quote(block):
    lines = block.split('\n')
    content = '\n'.join(line.lstrip('> ').rstrip() for line in lines)
    text_nodes = text_to_textnodes(content)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return ParentNode("blockquote", html_nodes)

def block_to_html_unordered_list(block):
        lines = block.split('\n')
        list_items = []
        for line in lines:
            content = line.lstrip('- ').rstrip()
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            list_items.append(ParentNode("li", html_nodes))
        return ParentNode("ul", list_items)

def block_to_html_ordered_list(block):
        lines = block.split('\n')
        list_items = []
        for line in lines:
            content = re.sub(r'^\d+\.\s', '', line).rstrip()
            text_nodes = text_to_textnodes(content)
            html_nodes = [text_node_to_html_node(node) for node in text_nodes]
            list_items.append(ParentNode("li", html_nodes))
        return ParentNode("ol", list_items)

def block_to_html_paragraph(block):
        text_nodes = text_to_textnodes(block)
        html_nodes = [text_node_to_html_node(node) for node in text_nodes]
        return ParentNode("p", html_nodes)

def markdown_to_html_node(markdown):
    blocks = BlockNode.markdown_to_blocks(markdown)
    html_nodes = []
    
    for block in blocks:
        block_type = BlockNode.block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            html_nodes.append(block_to_html_paragraph(block))
        elif block_type == BlockType.HEADING:
            html_nodes.append(block_to_html_heading(block))
        elif block_type == BlockType.CODE:
            html_nodes.append(block_to_html_code(block))
        elif block_type == BlockType.QUOTE:
            html_nodes.append(block_to_html_quote(block))
        elif block_type == BlockType.UNORDERED_LIST:
            html_nodes.append(block_to_html_unordered_list(block))
        elif block_type == BlockType.ORDERED_LIST:
            html_nodes.append(block_to_html_ordered_list(block))
    return ParentNode("div", html_nodes)
            
    

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # read markdown file from from_path
    # 'r' means read mode
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    
    
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    title = extract_title(markdown_content)
    
    html_content = markdown_to_html_node(markdown_content).to_html()
    
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    with open(dest_path, 'w') as file:
        file.write(final_html)