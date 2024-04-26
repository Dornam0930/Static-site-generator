import unittest
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link
)

class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        node = TextNode("Testing a **bold** word", text_type_text)
        converted_node = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(converted_node,
        [
            TextNode("Testing a ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" word", text_type_text)
        ]
        )
        #print(converted_node)

    def test_bold_multiword(self):
        node = TextNode("Testing multiple **bold** words, **here**, not here, and **here**", text_type_text)
        converted_node = split_nodes_delimiter([node], "**", text_type_bold)
        self.assertEqual(converted_node,
        [
            TextNode("Testing multiple ", text_type_text),
            TextNode("bold", text_type_bold),
            TextNode(" words, ", text_type_text),
            TextNode("here", text_type_bold),
            TextNode(", not here, and ", text_type_text),
            TextNode("here", text_type_bold),
        ]
        )
        #print(converted_node)
    
    def test_italic(self):
        node = TextNode("Testing a *italic* word", text_type_text)
        converted_node = split_nodes_delimiter([node], "*", text_type_italic)
        self.assertEqual(converted_node,
        [
            TextNode("Testing a ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word", text_type_text)
        ]
        )
        #print(converted_node)

    def test_code(self):
        node = TextNode("Testing a `code` word", text_type_text)
        converted_node = split_nodes_delimiter([node], "`", text_type_code)
        self.assertEqual(converted_node,
        [
            TextNode("Testing a ", text_type_text),
            TextNode("code", text_type_code),
            TextNode(" word", text_type_text)
        ]
        )
        #print(converted_node)

    def test_extract_markdown_images(self):
        sample_text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        searched_text = extract_markdown_images(sample_text)
        self.assertEqual(searched_text, [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])
        #print(searched_text)

    def test_extract_markdown_links(self):
        sample_text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        searched_text = extract_markdown_links(sample_text)
        self.assertEqual(searched_text, [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
        #print(searched_text)

    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            text_type_text,
        )
        new_nodes = split_nodes_image([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png")
        ])
        #print(new_nodes)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)",
            text_type_text
        )
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", text_type_text),
            TextNode("link", text_type_link, "https://www.example.com"),
            TextNode(" and ", text_type_text),
            TextNode("another", text_type_link, "https://www.example.com/another")
        ])
        #print(new_nodes)

    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)")
        self.assertEqual(nodes,
        [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ])
        #print(nodes)