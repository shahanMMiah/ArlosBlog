import unittest
import logging

import src.nodes.textnode as textnode
from src.nodes.textnode import TextNode
from src.nodes.leafnode import LeafNode


LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("testing node", "bold","www.test.com") 
        node2 = TextNode("testing node", "bold","www.test.com")

        self.assertEqual(node1,node2)

    def test_repr(self):

        node1 = TextNode("testing node", "bold","www.test.com") 
        
        self.assertIsInstance(node1.__repr__(),str)

    def test_attrs(self):
        node1 = TextNode(None,None,None)
        self.assertIsNotNone(node1.text)
        self.assertIsNotNone(node1.text_type)
        self.assertIsNotNone(node1.url)

    def test_text_to_html(self):
        
        node1 = TextNode("testing node", "bold","www.test.com") 
        hmtl_node1 = textnode.text_to_html_node(node1)
        LOG.info(f"{node1} is converted to {hmtl_node1.to_html()}")
        self.assertIsInstance(hmtl_node1, LeafNode)

        node2 = TextNode("testing italic node", "italic", None) 
        hmtl_node2 = textnode.text_to_html_node(node2)
        LOG.info(f"{node1} is converted to {hmtl_node2.to_html()}")
        self.assertIsInstance(hmtl_node2, LeafNode)


        node3 = TextNode("testing link node", "link", "www.testlink.com") 
        hmtl_node3 = textnode.text_to_html_node(node3)
        LOG.info(f"{node1} is converted to {hmtl_node3.to_html()}")
        self.assertIsInstance(hmtl_node3, LeafNode)
        
        node4 = TextNode("testing image node", "image", "www.testimage.com") 
        hmtl_node4 = textnode.text_to_html_node(node4)
        LOG.info(f"{node4} is converted to {hmtl_node4.to_html()}")
        self.assertIsInstance(hmtl_node4, LeafNode)
        
if __name__ == "__main__":
    unittest.main()