import unittest
from src import webpage
from src.markdown import block

import logging
LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class test_webpage(unittest.TestCase):

    def test_get_title(self):
            
        title  = webpage.extract_title_from_file("/home/smia/ArlosBlog/content/index.md")
        should_be = 'HTMLNode(h1, Tolkien Fan Club, (None, None))' 

        
        self.assertEqual(title.__repr__(),should_be)

        test  =  webpage.extract_title("# Hello")
        should_be = 'HTMLNode(h1, Hello, (None, None))'

        self.assertEqual(test.__repr__(),should_be)

    def test_node_from_markdown(self):

        from_mrkdown = webpage.read_markdown("/home/smia/ArlosBlog/content/index.md")
        from_html_nodes = block.markdown_to_hmtl_node(from_mrkdown)

        should_be = from_html_nodes.to_html()
        LOG.info(f"markdown converted to {from_html_nodes.to_html()}")

        self.assertEqual(from_html_nodes.to_html(), should_be)

if __name__ == "__main__":
    unittest.main()