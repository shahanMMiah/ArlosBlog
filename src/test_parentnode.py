import unittest
import logging

from leafnode import LeafNode
from parentnode import ParentNode


LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class TestParentNode(unittest.TestCase):
    
    def test_to_html(self):
        LOG.info("checking to hmtl outputs")
        
        node1 = ParentNode(
        "p",
        [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
        ],
        )

        test1 = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        LOG.info(f"{node1.to_html()} should match {test1}")
        
        self.assertEqual(node1.to_html(), test1)
        
        node2 = ParentNode(
        "p",
        [
            ParentNode(
                "p", 
                [
                    LeafNode(None, "Nested Normal text"),
                    LeafNode("i", "Nested italic text"),
                    LeafNode("b", "Nested bold text")]),

            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ],
        )

        test2 = "<p><p>Nested Normal text<i>Nested italic text</i><b>Nested bold text</b></p>Normal text<i>italic text</i>Normal text</p>"  
        LOG.info(f"{node2.to_html()} should match {test2}")
        
        self.assertEqual(node2.to_html(), test2)

    def check_missing_params(self):        
        LOG.info("checking is missing params")
        
        with self.assertRaises(AssertionError):
            
            test3= ParentNode("p")
            LOG.info(f"parent node errors if children is None")

            
        with self.assertRaises(ValueError):    
            node4 = ParentNode(None, [LeafNode(None, "Normal text"),])
            
            no_tag = node4.to_html()
            LOG.info(f"parent node errors if tag is None")
        

if __name__ == "__main__":
    unittest.main()