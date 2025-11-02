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
                