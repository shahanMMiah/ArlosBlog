import unittest

from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
    
        test1 =  '<p>This is a paragraph of text.</p>'
        test2 = '<a href="https://www.google.com">Click me!</a>'

        self.assertEqual(node1.to_html(), test1)
        self.assertEqual(node2.to_html(), test2)
        
if __name__ == "__main__":
    unittest.main()