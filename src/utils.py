import re

from htmlnode import ParentNode, block_to_html_node
from textnode import TextNode, TextType
from blocknode import BlockNode

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


def markdown_to_html_node(markdown):
    blocks = BlockNode.markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    with open(from_path, 'r') as file:
        markdown_content = file.read()
    
    with open(template_path, 'r') as file:
        template_content = file.read()
    
    title = extract_title(markdown_content)
    html_content = markdown_to_html_node(markdown_content).to_html()
    final_html = template_content.replace("{{ Title }}", title).replace("{{ Content }}", html_content)
    
    with open(dest_path, 'w') as file:
        file.write(final_html)