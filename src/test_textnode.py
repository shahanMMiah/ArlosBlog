import unittest

from textnode import TextNode

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
        print(node1)

    
        
if __name__ == "__main__":
    unittest.main()