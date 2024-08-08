import unittest

import src.markdown_utils as mk_utils

class TestMarkdownUtils(unittest.TestCase):
    
    def test_extract_images(self):
        
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
 
        extracted_images = mk_utils.extract_markdown_images(text)

        should_be = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(extracted_images, should_be)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        
        extracted_links = mk_utils.extract_markdown_links(text)

        should_be = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        self.assertEqual(extracted_links, should_be)

    def test_markdown_to_block(self):

        test_str =  """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """

        blocks = mk_utils.markdown_to_blocks(test_str)

        should_be  = ["# This is a heading",
                      "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                      "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
                    ]
        print(blocks)
        self.assertEqual(blocks,should_be)


if __name__ == "__main__":
    unittest.main()