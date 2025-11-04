

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