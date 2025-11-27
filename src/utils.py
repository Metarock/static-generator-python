import re
import os 

from htmlnode import LeafNode, ParentNode, text_node_to_html_node
from textnode import TextNode, TextType
from blocknode import BlockNode, BlockType

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No h1 header found in markdown")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.node_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
    return new_nodes

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r'\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.node_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            matches = extract_markdown_images(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                parts = re.split(r'!\[[^\]]*\]\([^)]+\)', node.text)
                for i in range(len(parts)):
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
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
            matches = extract_markdown_links(node.text)
            if not matches:
                new_nodes.append(node)
            else:
                parts = re.split(r'\[[^\]]*\]\([^)]+\)', node.text)
                for i in range(len(parts)):
                    if parts[i]:
                        new_nodes.append(TextNode(parts[i], TextType.TEXT))
                    if i < len(matches):
                        link_text, url = matches[i]
                        link_node = TextNode(link_text, TextType.LINK)
                        link_node.url = url
                        new_nodes.append(link_node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_html_node(block):
    block_type = BlockNode.block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.ORDERED_LIST:
        return olist_to_html_node(block)
    if block_type == BlockType.UNORDERED_LIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def markdown_to_html_node(markdown):
    blocks = BlockNode.markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    title = extract_title(markdown_content)
    html_content = markdown_to_html_node(markdown_content).to_html()
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)

    final_html = final_html.replace('href="/', 'href="' + basepath)
    final_html = final_html.replace('src="/', 'src="' + basepath)
    
    with open(dest_path, 'w') as file:
        file.write(final_html)
        

def generate_pages_recursive(dir_path_content, template_path, dir_path_dest, basepath):
    # crawl every entry in the content directory
    for entry in os.listdir(dir_path_content):
        src_entry_path = os.path.join(dir_path_content, entry)
        dest_entry_path = os.path.join(dir_path_dest, entry)
        
        if os.path.isdir(src_entry_path):
            if not os.path.exists(dest_entry_path):
                os.makedirs(dest_entry_path)
            generate_pages_recursive(src_entry_path, template_path, dest_entry_path, basepath)
        elif entry.endswith('.md'):
            file_name = dest_entry_path[:-3]
            dest_html_path = file_name + '.html'
            generate_page(src_entry_path, template_path, dest_html_path, basepath)        
