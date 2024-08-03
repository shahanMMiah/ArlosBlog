import unittest
import logging

import src.delimiter as delimiter
import src.textnode as textnode


LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class TestDelimiter(unittest.TestCase):

    def test_delimit(self):
        node = textnode.TextNode("This is text with a `code block` word", textnode.TextTypes.text_type_text.value, None)
        new_nodes = delimiter.split_nodes_delimiter([node], "`", textnode.TextTypes.text_type_code.value)

        nodes_test = [
            textnode.TextNode("This is text with a ", "text", None ),
                textnode.TextNode("code block", "code",None ), 
                textnode.TextNode(" word", "text", None )
            ]
        
        LOG.info(f"{new_nodes} should match {nodes_test}")
        self.assertEqual(new_nodes, nodes_test)
        
    def test_multiple_text_nodes(self):
        nodes = [
            textnode.TextNode("test 1 * this part is bold* line",textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("test 2 **this part is bold?** line",textnode.TextTypes.text_type_bold.value,None),
            textnode.TextNode("test 3 * this part should be code* line",textnode.TextTypes.text_type_code.value,None)
            ]
        
        delimit_nodes = delimiter.split_nodes_delimiter(nodes, "*",textnode.TextTypes.text_type_bold.value)

        should_be = [       
                textnode.TextNode("test 1 ",textnode.TextTypes.text_type_text.value,None),
                textnode.TextNode(" this part is bold",textnode.TextTypes.text_type_bold.value,None),
                textnode.TextNode(" line",textnode.TextTypes.text_type_text.value,None),
                textnode.TextNode("test 2 **this part is bold?** line",textnode.TextTypes.text_type_bold.value,None),
                textnode.TextNode("test 3 * this part should be code* line",textnode.TextTypes.text_type_code.value,None)]
        LOG.info(f"multiple_text_nodes looks like {delimit_nodes}")
        
        self.assertEqual(delimit_nodes, should_be) 
    
    def test_no_closing_delimiter(self):
        node = textnode.TextNode("this line has no * closing delim", textnode.TextTypes.text_type_text.value,None )
        node2 = textnode.TextNode("this line * also has* no * closing delim", textnode.TextTypes.text_type_text.value,None )
    
        with self.assertRaises(RuntimeError):
            delimiter.split_nodes_delimiter([node],"*",textnode.TextTypes.text_type_italic.value)
            delimiter.split_nodes_delimiter([node2],"*",textnode.TextTypes.text_type_italic.value)
    
    def test_multiple_split(self):
        node1 = textnode.TextNode(
            " this should have *multiple code* blocks * that are outputed* for this",textnode.TextTypes.text_type_text.value,None)
    
        delimit_nodes = delimiter.split_nodes_delimiter([node1], "*",textnode.TextTypes.text_type_code.value)

        should_be = [
            textnode.TextNode(
            " this should have ",textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode(
            "multiple code",textnode.TextTypes.text_type_code.value,None),
            textnode.TextNode(
            " blocks ",textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode(
            " that are outputed",textnode.TextTypes.text_type_code.value,None),
            textnode.TextNode(
            " for this",textnode.TextTypes.text_type_text.value,None)
        ]

        LOG.info(f"multiple split test looks like {delimit_nodes}")
        
        self.assertEqual(delimit_nodes, should_be) 


        
    

if __name__ == "__main__":
    unittest.main()