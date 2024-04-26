import re
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        finished_nodes = []
        split_node = node.text.split(delimiter)
        if len(split_node) % 2 == 0:
            raise ValueError("Invalid markdown syntax: markdown section is not closed")
        for i in range(len(split_node)):
            if split_node[i] == "":
                continue
            if i % 2 == 0:
                finished_nodes.append(TextNode(split_node[i], text_type_text))
            else:
                finished_nodes.append(TextNode(split_node[i], text_type))
        new_nodes.extend(finished_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return matches

def  split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        old_text = node.text
        images = list(extract_markdown_images(old_text))
        if len(images) == 0:
            new_nodes.append(node)
            continue
        for image in images:
            split_text = old_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, image syntax not closed")
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(image[0], text_type_image, image[1]))
            old_text = split_text[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, text_type_text))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != text_type_text:
            new_nodes.append(node)
            continue
        old_text = node.text
        links = extract_markdown_links(old_text)
        if len(links) == 0:
            new_nodes.append(node)
            continue
        for link in links:
            split_text = old_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown, link syntax not closed", 1)
            if split_text[0] != "":
                new_nodes.append(TextNode(split_text[0], text_type_text))
            new_nodes.append(TextNode(link[0], text_type_link, link[1]))
            old_text = split_text[1]
        if old_text != "":
            new_nodes.append(TextNode(old_text, text_type_text))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, text_type_text)]
    nodes = split_nodes_delimiter(nodes, "**", text_type_bold)
    nodes = split_nodes_delimiter(nodes, "*", text_type_italic)
    nodes = split_nodes_delimiter(nodes, "`", text_type_code)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes