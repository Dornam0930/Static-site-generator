from markdown_blocks import markdown_to_html_node
from htmlnode import ParentNode
import os

md_file_type = ".md"
html_file_type = ".html"

def extract_title(markdown):
    header = markdown.split("\n", 1)[0]
    if header[0:2] != "# ":
        raise Exception("Error: no h1 header at start of file")
    html_header = markdown_to_html_node(header).to_html()
    return html_header

def generate_page(from_path, template_path, dest_path, file_name):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown_doc = f.read()
    #markdown_doc = open(from_path)
    with open(template_path) as g:
        template_doc = g.read()
    #template_doc = open(template_path)
    parent = markdown_to_html_node(markdown_doc)
    children = parent.to_html()
    title = extract_title(markdown_doc)
    html_doc = template_doc.replace("{{ Content }}", children)
    html_doc = html_doc.replace("{{ Title }}", title)
    if not os.path.exists(dest_path):
        os.makedirs(dest_path, exist_ok=True)
    with open(os.path.join(dest_path, file_name), "w+") as h:
        h.write(html_doc)

def generate_pages_recursively(from_path, template_path, dest_path):
    file_list = os.listdir(from_path)
    print(file_list)
    for file in file_list:
        file_path = os.path.join(from_path, file)
        if os.path.isfile(file_path):
            if file[-3:] == md_file_type:
                file = file[:-3] + html_file_type
                print(file)
            print(f"Generating page: {dest_path}/{file}")
            generate_page(file_path, template_path, dest_path, file)
        if os.path.isdir(file_path):
            print(f"Making new subdirectory: {dest_path}/{file}")
            generate_pages_recursively(os.path.join(from_path, file), template_path, os.path.join(dest_path, file))