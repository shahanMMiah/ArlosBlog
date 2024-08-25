"""block module unit tests"""

import os
import unittest
import logging
import locale

import src.markdown.block as block
from src import datatypes

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


class TestBlock(unittest.TestCase):
    """testing block module functions test cases"""

    def test_markdown_to_block(self):
        """testing basic string converted to block list"""

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
        LOG.info("markdown blocks are %s", blocks)
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
        LOG.info(" %s block is %s", heading_check, blocks[0])
        self.assertEqual(heading_check, datatypes.BlockTypes.HEADING_NAME.value)

        para_check = block.block_to_block_type(blocks[1])
        LOG.info("%s block is %s", para_check, blocks[1])
        self.assertEqual(para_check, datatypes.BlockTypes.PARAGRAPH_NAME.value)

        code_check = block.block_to_block_type(blocks[2])
        LOG.info("%s block is %s", code_check, blocks[2])
        self.assertEqual(code_check, datatypes.BlockTypes.CODE_NAME.value)

        qoute_check = block.block_to_block_type(blocks[3])
        LOG.info("%s block is %s", qoute_check, blocks[3])
        self.assertEqual(qoute_check, datatypes.BlockTypes.QOUTE_NAME.value)

        unord_lis_check = block.block_to_block_type(blocks[4])
        LOG.info("%s block is %s", unord_lis_check, blocks[4])
        self.assertEqual(unord_lis_check, datatypes.BlockTypes.UNORDERED_NAME.value)

        ord_lis_check = block.block_to_block_type(blocks[5])
        LOG.info("%s block is %s", ord_lis_check, blocks[5])
        self.assertEqual(ord_lis_check, datatypes.BlockTypes.ORDERED_NAME.value)

    def test_markdown_to_nodes(self):

        test_str = """# This is a heading

        This is a paragraph of text. It has some **bold** and *italic* words inside of it.  

        ``` this is code block ```

        > this is a quote block   

        * This is the first list item *in a list block*    
        * This is a list item    
        * This is another list item

        1. thi is a first in ord list
        2. second in ord list
        
        """

        test_node_tree = block.markdown_to_hmtl_node(test_str)

        LOG.info("test block to hmtl nodes is %s", test_node_tree.to_html())
        self.assertIsInstance(test_node_tree.to_html(), str)

        test_str_2 = """ * I really
            * hate writing *italic font*
            * in raw html
        """
        to_hmtl = block.markdown_to_hmtl_node(test_str_2)
        hmtl_str = """<div><ul><li>I really</li><li>hate writing <i>italic font</i></li><li>in raw html</li></ul></div>"""

        LOG.info("test block to hmtl 2 nodes is %s", to_hmtl.to_html())
        self.assertEqual(to_hmtl.to_html(), hmtl_str)

        test_str_3 = """ 1. I really
            2. hate writing *italic font*
            3. in raw html
        """
        to_hmtl3 = block.markdown_to_hmtl_node(test_str_3)
        hmt3_str = """<div><ol><li>I really</li><li>hate writing <i>italic font</i></li><li>in raw html</li></ol></div>"""

        LOG.info("test block to hmtl 3 nodes is %s", to_hmtl3.to_html())
        self.assertEqual(to_hmtl3.to_html(), hmt3_str)

    def test_html_nodes_contains(self):

        mk1 = str()

        with open(
            os.path.join(PROJECT_DIR, "content", "index.md"),
            "r",
            encoding=locale.getpreferredencoding(),
        ) as mk_obj:
            mk1 = mk_obj.read()

        hmtl1 = block.markdown_to_hmtl_node(mk1)

        mk1_checks = [
            "<h1>Tolkien Fan Club</h1>",
            "<li>Gandalf</li>",
            "<i>didn't ruin it</i>",
            "<b>I like Tolkien</b>",
            "<a href",
            "<li>It can be enjoyed by children and adults alike</li>",
            "<code>",
            "<blockquote>All that is gold does not glitter</blockquote>",
        ]

        for check in mk1_checks:
            self.assertIn(check, hmtl1.to_html())
        LOG.info("index file 1 passed all checks")

        mk2 = str()

        with open(
            os.path.join(PROJECT_DIR, "content", "majesty", "index.md"),
            "r",
            encoding=locale.getpreferredencoding(),
        ) as mk_obj:
            mk2 = mk_obj.read()

        hmtl2 = block.markdown_to_hmtl_node(mk2)

        mk2_checks = [
            "<h1>The Unparalleled Majesty",
            "<b>Archmage</b>",
            "<code>Valar</code>",
            "<i>legendarium</i>",
            "<a href",
        ]

        for check in mk2_checks:
            self.assertIn(check, hmtl2.to_html())
        LOG.info("index file 2 passed all checks")


if __name__ == "__main__":
    unittest.main()
