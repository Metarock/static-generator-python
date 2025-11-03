import re

from textnode import TextNode, TextType

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