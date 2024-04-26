import unittest

from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote
    )

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
        """
        text2 = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
        """
        blocks = markdown_to_blocks(text)
        blocks2 = markdown_to_blocks(text2)
        self.assertEqual(
            blocks,[
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is a list item\n* This is another list item"
        ])
        self.assertEqual(
            blocks2,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items"
            ]
        )

    def test_block_to_block_type(self):
        block = "### heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```code```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = ">quote\n>quote2"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "-list\n*list2"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. ordered\n2. list"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)