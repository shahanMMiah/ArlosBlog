from .. import datatypes
from .leafnode import LeafNode

    
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
        case(datatypes.TextTypes.TEXT_NAME.value):
            return(LeafNode(
                tag=None, 
                value=text_node.text, 
                props=None))
        case(datatypes.TextTypes.BOLD_NAME.value):
            return(
            LeafNode(
                tag=datatypes.InlineTypes.BOLD_TAG.value, 
                value=text_node.text.lstrip(" ").rstrip(" "), 
                props=None))
        case(datatypes.TextTypes.ITALIC_NAME.value):
            return(
            LeafNode(
                tag=datatypes.InlineTypes.ITALIC_TAG.value, 
                value=text_node.text.lstrip(" ").rstrip(" "), 
                props=None))
        case(datatypes.TextTypes.CODE_NAME.value):
            return(
            LeafNode(
                tag=datatypes.TextTypes.CODE_NAME.value,
                value=text_node.text.lstrip(" ").rstrip(" "), 
                props=None))

        case(datatypes.TextTypes.LINK_NAME.value):
            return(
            LeafNode(
                tag=datatypes.InlineTypes.LINK_TAG.value, 
                value=text_node.text, 
                props={"href":text_node.url}))

        case(datatypes.TextTypes.IMAGE_NAME.value):
            return(
            LeafNode(
                tag=datatypes.InlineTypes.IMAGE_TAG.value, 
                value="anchor text", 
                props={
                    "src":text_node.url, 
                    "alt":text_node.text
                    }))
        case _:
            raise Exception("type not reconised")


   