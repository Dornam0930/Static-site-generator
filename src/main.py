from textnode import TextNode
import os, shutil
from generate_page import generate_page, generate_pages_recursively

dir_path_static = "./static"
dir_path_content = "./content"
dir_path_public = "./public"
template_path = "./template.html"


def main():
    copy_files(dir_path_static, dir_path_public)

    generate_pages_recursively(dir_path_content, template_path, dir_path_public)

    #generate_page(os.path.join(dir_path_content, "index.md"), template_path, dir_path_public)
    #text_node_1 = TextNode("This is a text node", "bold", "https://www.boot.dev")
    #print(repr(text_node_1))

    #copy_files("D:/My Stuff/Programming/Python/Static site/static", "D:/My Stuff/Programming/Python/Static site/public")

    #generate_page("D:/My Stuff/Programming/Python/Static site/content/index.md", "D:/My Stuff/Programming/Python/Static site/template.html", "D:/My Stuff/Programming/Python/Static site/public")

    #generate_page("D:/My Stuff/Programming/Python/Static site/content/index2.md", "D:/My Stuff/Programming/Python/Static site/template.html", "D:/My Stuff/Programming/Python/Static site/public")

def copy_files(from_directory, to_directory):
    if not os.path.exists(from_directory):
        raise ValueError(f"Invalid source file path: '{from_directory}' does not exist")
    if not os.path.exists(to_directory):
        os.mkdir(to_directory)
        print(f"Making new to directory: {to_directory}")
    else:
        files_to_delete = os.listdir(to_directory)
        if len(files_to_delete) != 0:
            for file_to_delete in files_to_delete:
                delete_path = os.path.join(to_directory,file_to_delete)
                if os.path.isdir(delete_path):
                    shutil.rmtree(delete_path)
                    print(f"Deleting sub to directory: {delete_path}")
                else:
                    os.remove(delete_path)
                    print(f"Deleting file in to directory: {delete_path}")
    file_list = os.listdir(from_directory)
    for file in file_list:
        old_path = os.path.join(from_directory, file)
        new_path = os.path.join(to_directory, file)
        if os.path.isdir(old_path):
            print(f"Calling copy_files recursively for {file} folder")
            copy_files(old_path, new_path)
        else:
            shutil.copy(old_path, new_path)
            print(f"Copying {file} to {to_directory}")
    print("Ending one cycle of copy_files")

main()
