import unittest

from src.nodes.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_repr(self):

        node1 = HTMLNode(tag ="p", value="test paragraph",children=None, props={"href": "https://www.google.com"}) 
        
        self.assertIsInstance(node1.__repr__(),str)

    def test_props_to_hmtl(self):

       node1 = HTMLNode(tag ="p", value="test paragraph",children=None, props={"href": "https://www.google.com"})

       self.assertIsInstance(node1.props_to_html(),str)

    def test_to_hmtl(self):
        node1 = HTMLNode(tag ="p", value="test paragraph",children=None, props={"href": "https://www.google.com"}) 

        with self.assertRaises( NotImplementedError):
            node1.to_html()

    
        
if __name__ == "__main__":
    unittest.main()