import unittest
import logging

import src.markdown.inline as inline
import src.nodes.textnode as textnode


LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

class Testinline(unittest.TestCase):

    def test_delimit(self):
        node = textnode.TextNode("This is text with a `code block` word", textnode.TextTypes.text_type_text.value, None)
        new_nodes = inline.split_nodes_delimiter([node], "`", textnode.TextTypes.text_type_code.value)

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
        
        delimit_nodes = inline.split_nodes_delimiter(nodes, "*",textnode.TextTypes.text_type_bold.value)

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
            inline.split_nodes_delimiter([node],"*",textnode.TextTypes.text_type_italic.value)
            inline.split_nodes_delimiter([node2],"*",textnode.TextTypes.text_type_italic.value)
    
    def test_multiple_split(self):
        node1 = textnode.TextNode(
            " this should have *multiple code* blocks * that are outputed* for this",textnode.TextTypes.text_type_text.value,None)
    
        delimit_nodes = inline.split_nodes_delimiter([node1], "*",textnode.TextTypes.text_type_code.value)

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

    def test_start_end_delimits(self):
        start_node = textnode.TextNode(
            "*this should have * a start code block",textnode.TextTypes.text_type_text.value,None)
        
        end_node = textnode.TextNode(
            " this should have a *end code block*",textnode.TextTypes.text_type_text.value,None)
        
        start_delimit = inline.split_nodes_delimiter([start_node], "*",textnode.TextTypes.text_type_code.value)
        end_delimit = inline.split_nodes_delimiter([end_node], "*",textnode.TextTypes.text_type_code.value)

        start_should_be = [
            textnode.TextNode(
            "this should have ",textnode.TextTypes.text_type_code.value,None),
            textnode.TextNode(
            " a start code block",textnode.TextTypes.text_type_text.value,None),
        ]

        end_should_be = [
            textnode.TextNode(
            " this should have a ",textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode(
            "end code block",textnode.TextTypes.text_type_code.value,None),
        ]

        LOG.info(f"testing delimets at start {start_delimit} and end {end_delimit}")
        self.assertEqual(start_delimit, start_should_be)
        self.assertEqual(end_delimit, end_should_be)
        
    
    def test_split_nodes_links(self):
        

        node = textnode.TextNode("[to boot dev](https://www.boot.dev) This is text with a link and [to youtube](https://www.youtube.com/@bootdotdev) huh",
        textnode.TextTypes.text_type_text.value, None)
        
        new_nodes = inline.split_nodes_links([node])

        should_be = [
            textnode.TextNode("to boot dev", textnode.TextTypes.text_type_link.value, "https://www.boot.dev"),
            textnode.TextNode(" This is text with a link and ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("to youtube", textnode.TextTypes.text_type_link.value, "https://www.youtube.com/@bootdotdev"),
            textnode.TextNode(" huh", textnode.TextTypes.text_type_text.value,None)
        ]       
        LOG.info(f"new_nodes is {new_nodes}")
        self.assertEqual(new_nodes, should_be)

        node2 = textnode.TextNode("[to boot dev](https://www.boot.dev) This is text [with a middle link](https://www.middlelink.com) a link and [to youtube](https://www.youtube.com/@bootdotdev) huh",
        textnode.TextTypes.text_type_text.value, None)
        should_be_2 = [
            textnode.TextNode("to boot dev", textnode.TextTypes.text_type_link.value, "https://www.boot.dev"),
            textnode.TextNode(" This is text ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("with a middle link", textnode.TextTypes.text_type_link.value, "https://www.middlelink.com"),
            textnode.TextNode(" a link and ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("to youtube", textnode.TextTypes.text_type_link.value, "https://www.youtube.com/@bootdotdev"),
            textnode.TextNode(" huh", textnode.TextTypes.text_type_text.value,None)
        ]  
        
        new_nodes2 = inline.split_nodes_links([node2])

        self.assertEqual(new_nodes2, should_be_2)

    
    def test_split_images(self):
        
        img_node = textnode.TextNode(
            "This is a with image and ![image anchor](image_urls/images)",textnode.TextTypes.text_type_text.value,None)
        
        new_img_node = inline.split_nodes_images([img_node])
        img_test = [
            textnode.TextNode("This is a with image and ", textnode.TextTypes.text_type_text.value, None),
            textnode.TextNode("image anchor",  textnode.TextTypes.text_type_image.value, "image_urls/images")
            ]
        self.assertEqual(new_img_node,img_test)
        
        img_node_2 = textnode.TextNode("![boot img](https://www.boot.dev/img) This is a image and ![youtube logo](https://www.youtube.com/logo)",
        textnode.TextTypes.text_type_text.value, None)
        
        img_new_node_2 = inline.split_nodes_images([img_node_2])

        should_be_2 = [
            textnode.TextNode("boot img", textnode.TextTypes.text_type_image.value, "https://www.boot.dev/img"),
            textnode.TextNode(" This is a image and ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("youtube logo", textnode.TextTypes.text_type_image.value, "https://www.youtube.com/logo"),
        ]       
        LOG.info(f"img list is {img_new_node_2}")   
        self.assertEqual(img_new_node_2, should_be_2)

    def test_text_to_textnodes(self):
        text_str = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        
        text_nodes = inline.text_to_textnode(text_str)
        
        should_be = [
            textnode.TextNode("This is ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("text", textnode.TextTypes.text_type_bold.value,None),
            textnode.TextNode(" with an ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("italic", textnode.TextTypes.text_type_italic.value,None),
            textnode.TextNode(" word and a ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("code block", textnode.TextTypes.text_type_code.value,None),
            textnode.TextNode(" and an ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("obi wan image", textnode.TextTypes.text_type_image.value, "https://i.imgur.com/fJRm4Vk.jpeg"),
            textnode.TextNode(" and a ", textnode.TextTypes.text_type_text.value,None),
            textnode.TextNode("link", textnode.TextTypes.text_type_link.value, "https://boot.dev"),
        ]
        LOG.info(f"text to textnodes is {text_nodes}") 
        self.assertEqual(text_nodes, should_be)

    
    def test_extract_images(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        extracted_images = inline.extract_markdown_images(text)

        should_be = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertEqual(extracted_images, should_be)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        extracted_links = inline.extract_markdown_links(text)

        should_be = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(extracted_links, should_be)


if __name__ == "__main__":
    unittest.main()