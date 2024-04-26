from inline_markdown import text_to_textnodes
from htmlnode import ParentNode
from textnode import text_node_to_html_node

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    lines = markdown.split("\n\n")
    finished_lines = []
    for line in lines:
        if line == "":
            continue
        finished_lines.append(line.strip())
    return finished_lines

def block_to_block_type(block):
    lines = block.split("\n")
    if block[0] == "#":
        i = 0
        for letter in block:
            if letter == "#":
                i += 1
                continue
            if letter == " ":
                return block_type_heading
            if i == 7:
                return block_type_paragraph
        return block_type_heading
    if block[0:3] == "```" and block[-3:] == "```":
        return block_type_code
    if block[0] == ">":
        for line in lines:
            if line[0] != ">":
                return block_type_paragraph
        return block_type_quote
    if block[0] == "-":
        for line in lines:
            if line[0] != "-":
                return block_type_paragraph
            return block_type_unordered_list
    if block[0] == "*":
        for line in lines:
            if line[0] != "*":
                return block_type_paragraph
            return block_type_unordered_list
    if block[0:2] == "1.":
        for i in range(1,len(lines)):
            if lines[i][0:2] != f"{i + 1}.":
                return block_type_paragraph
        return block_type_ordered_list
    return block_type_paragraph

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        children.append(block_to_HTMLNode(block))
    return ParentNode("div", children, None)

def block_to_HTMLNode(block):
    block_type = block_to_block_type(block)
    if block_type == block_type_paragraph:
        return block_to_paragraph_node(block)
    if block_type == block_type_heading:
        return block_to_heading_node(block)
    if block_type == block_type_code:
        return block_to_code_node(block)
    if block_type == block_type_quote:
        return block_to_quote_node(block)
    if block_type == block_type_unordered_list:
        return block_to_ulist_node(block)
    if block_type == block_type_ordered_list:
        return block_to_olist_node(block)

def block_to_paragraph_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def block_to_heading_node(block):
    style = 0
    for letter in block:
        if letter == "#":
            style += 1
        else:
            break
    if style + 1 > len(block):
        raise ValueError("Invalid heading: no letters after heading syntax")
    children = text_to_children(block[style + 1:])
    return ParentNode(f"h{style}", children)

def block_to_code_node(block):
    if block[0:3] != "```" or block[-3:] != "```":
        raise ValueError("Invalid code block")
    children = text_to_children(block[3:-3])
    code = ParentNode("code", children)
    return ParentNode("pre", [code])

def block_to_quote_node(block):
    lines = block.split("\n")
    stripped_lines = []
    for line in lines:
        if line[0] != ">":
            raise ValueError("Invalid quote block")
        stripped_lines.append(line.lstrip(">").strip())
    joined_lines = " ".join(stripped_lines)
    children = text_to_children(joined_lines)
    return ParentNode("blockquote", children)

def block_to_ulist_node(block):
    lines = block.split("\n")
    ulist_nodes = []
    for line in lines:
        ulist_nodes.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", ulist_nodes)
        
def block_to_olist_node(block):
    lines = block.split("\n")
    olist_nodes = []
    for line in lines:
        olist_nodes.append(ParentNode("li", text_to_children(line[2:])))
    return  ParentNode("ol", olist_nodes)

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        children.append(text_node_to_html_node(text_node))
    return children