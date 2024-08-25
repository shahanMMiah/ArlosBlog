""" Leaf HMTL node class"""

from .htmlnode import HTMLNode


class LeafNode(HTMLNode):
    """Leaf HMTL node class

    Args:
        HTMLNode (HTMLNode): base HMTL class
    """

    def __init__(self, tag, value, props=None):
        super(LeafNode, self).__init__(value=value, children=None, tag=tag, props=props)
        if not self.value:
            raise ValueError("value is required")

    def to_html(self):
        """return HMTL code of node as str

        Raises:
            ValueError: No node value provided

        Returns:
            str: hmtl repersentation of code
        """
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return str(self.value)

        html_str = self.start_tag
        if self.props:

            for key, val in self.props.items():
                html_str = html_str.replace(">", f' {key}="{val}">')

        html_str += f"{self.value}{self.end_tag}"

        return html_str
