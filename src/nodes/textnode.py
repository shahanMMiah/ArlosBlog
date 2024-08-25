""" Text node class, for converting str to hmtl types

Raises:
    Exception: text type not recognised
"""

from .. import datatypes
from .leafnode import LeafNode


class TextNode:
    """TextNode class"""

    def __init__(self, text, text_type, url):
        self.text = text or ""
        self.text_type = text_type or ""
        self.url = url or ""

    def __eq__(self, textnode):
        """equal operator overide, compares text, type and url

        Args:
            textnode (Textnode): text node to compare to
        """
        return (
            self.text == textnode.text
            and self.text_type == textnode.text_type
            and self.url == textnode.url
        )

    def __repr__(self):
        """print override, print text, type and url"""
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_to_html_node(text_node):
    """checks text node type and returns HMTL node of same type

    Args:
        text_node (TextNode): textnode to check

    Raises:
        Exception: type not recognised
    """

    match (text_node.text_type):
        case datatypes.TextTypes.TEXT_NAME.value:
            return LeafNode(tag=None, value=text_node.text, props=None)
        case datatypes.TextTypes.BOLD_NAME.value:
            return LeafNode(
                tag=datatypes.InlineTypes.BOLD_TAG.value,
                value=text_node.text.lstrip(" ").rstrip(" "),
                props=None,
            )
        case datatypes.TextTypes.ITALIC_NAME.value:
            return LeafNode(
                tag=datatypes.InlineTypes.ITALIC_TAG.value,
                value=text_node.text.lstrip(" ").rstrip(" "),
                props=None,
            )
        case datatypes.TextTypes.CODE_NAME.value:
            return LeafNode(
                tag=datatypes.TextTypes.CODE_NAME.value,
                value=text_node.text.lstrip(" ").rstrip(" "),
                props=None,
            )

        case datatypes.TextTypes.LINK_NAME.value:
            return LeafNode(
                tag=datatypes.InlineTypes.LINK_TAG.value,
                value=text_node.text,
                props={"href": text_node.url},
            )

        case datatypes.TextTypes.IMAGE_NAME.value:
            return LeafNode(
                tag=datatypes.InlineTypes.IMAGE_TAG.value,
                value=" ",
                props={"src": text_node.url, "alt": text_node.text},
            )
        case _:
            raise ValueError("type not reconised")
