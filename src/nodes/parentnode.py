""" Parent HMTL node class, HTML type with children and no value."""

from .htmlnode import HTMLNode
from .. import datatypes


class ParentNode(HTMLNode):
    """parent HMTL node class

    Args:
        HTMLNode (HTMLNode): base HMTL class
    """

    def __init__(self, tag=None, children=None, props=None):
        assert children is not None
        super(ParentNode, self).__init__(
            children=children, tag=tag, value=None, props=props
        )

    def to_html(self, output_str=""):
        """return HMTL code of node as str

        Raises:
            ValueError: No node tag provided
        Raises:
            ValueError: No node children provided

        Returns:
            str: hmtl repersentation of code
        """

        if not self.tag:
            raise ValueError(f"{self} has no tag")
        if not self.children:
            raise ValueError(f"{self} has no children")

        if self.tag != datatypes.TextTypes.NULL_NAME.value:
            output_str += self.start_tag

        for childs in self.children:
            if isinstance(childs, ParentNode):
                output_str = childs.to_html(output_str=output_str)
            else:
                output_str += childs.to_html()

        if self.tag != datatypes.TextTypes.NULL_NAME.value:
            output_str += self.end_tag

        return output_str
