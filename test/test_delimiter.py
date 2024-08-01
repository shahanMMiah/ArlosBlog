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
        

if __name__ == "__main__":
    unittest.main()