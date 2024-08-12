import unittest
import logging

import src.markdown.block as block

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class TestBlock(unittest.TestCase):

    def test_markdown_to_block(self):

        test_str = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.

        * This is the first list item in a list block
        * This is a list item
        * This is another list item
        """

        blocks = block.markdown_to_blocks(test_str)

        should_be = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        LOG.info(f"markdown blocks are {blocks}")
        self.assertEqual(blocks, should_be)

    def test_remove_white_space_block(self):
        
        test_str = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.     

        * This is the first list item in a list block    
        * This is a list item    
        * This is another list item    
        """

        blocks = block.markdown_to_blocks(test_str)

        should_be = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(blocks, should_be)

    def test_block_types(self):
        
        test_str = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.  

        ``` this is code block

        > this is a quote block   

        * This is the first list item in a list block    
        * This is a list item    
        * This is another list item

        1. thi is a first in ord list
        2. second in ord list
        
        """

        blocks = block.markdown_to_blocks(test_str)

        
        heading_check = block.block_to_block_type(blocks[0])
        LOG.info(f"{heading_check} block is {blocks[0]}")
        self.assertEqual(heading_check, block.BlockTypes.HEADING_NAME.value)
        
        
        para_check  = block.block_to_block_type(blocks[1])
        LOG.info(f"{para_check} block is {blocks[1]}")
        self.assertEqual(para_check, block.BlockTypes.PARAGRAPH_NAME.value)

        
        code_check = block.block_to_block_type(blocks[2])
        LOG.info(f"{code_check} block is {blocks[2]}")
        self.assertEqual(code_check, block.BlockTypes.CODE_NAME.value)
        
        
        qoute_check = block.block_to_block_type(blocks[3])
        LOG.info(f"{qoute_check} block is {blocks[3]}")
        self.assertEqual(qoute_check, block.BlockTypes.QOUTE_NAME.value)

        unord_lis_check = block.block_to_block_type(blocks[4])
        LOG.info(f"{unord_lis_check} block is {blocks[4]}")
        self.assertEqual(unord_lis_check, block.BlockTypes.UNORDERED_NAME.value)
        
        ord_lis_check = block.block_to_block_type(blocks[5])
        LOG.info(f"{ord_lis_check} list block is {blocks[5]}")
        self.assertEqual(ord_lis_check, block.BlockTypes.ORDERED_NAME.value)





if __name__ == "__main__":
    unittest.main()
