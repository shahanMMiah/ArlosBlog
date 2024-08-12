from enum import Enum
from .leafnode import LeafNode

class TextTypes(Enum):
    text_type_text = "text"
    text_type_bold = "bold"
    text_type_italic = "italic"
    text_type_code = "code"
    text_type_link = "link"
    text_type_image = "image"

    
class TextNode():
    def __init__(self, text, text_type, url):
        self.text = text or ""
        self.text_type = text_type or ""
        self.url = url or ""
    
    def __eq__(self, textNode):
        return(
                self.text == textNode.text and 
                self.text_type == textNode.text_type and
                self.url == textNode.url
                )
    
    def __repr__(self):
        return(
            f"TextNode({self.text}, {self.text_type}, {self.url})"
            )

def text_to_html_node(text_node):
   
    match(text_node.text_type):
        case(TextTypes.text_type_text.value):
            return(LeafNode(
                tag=None, 
                value=text_node.text, 
                props=None))
        case(TextTypes.text_type_bold.value):
            return(
            LeafNode(
                tag="b", 
                value=text_node.text, 
                props=None))
        case(TextTypes.text_type_italic.value):
            return(
            LeafNode(
                tag="i", 
                value=text_node.text, 
                props=None))
        case(TextTypes.text_type_code.value):
            return(
            LeafNode(
                tag="code",
                value=text_node.text, 
                props=None))

        case(TextTypes.text_type_link.value):
            return(
            LeafNode(
                tag="a", 
                value=text_node.text, 
                props={"href":text_node.url}))

        case(TextTypes.text_type_image.value):
            return(
            LeafNode(
                tag="img", 
                value="anchor text", 
                props={
                    "src":text_node.url, 
                    "alt":text_node.text
                    }))
        case _:
            raise Exception("type not reconised")


   