"""HMTL base class

Raises:
    NotImplementedError: to_hmtl to be implemented by derived classes
"""


class HTMLNode:
    """HMTL base class"""

    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    @property
    def start_tag(self):
        """start tag of hmtl string"""
        start_tag = f"<{self.tag}>"
        if self.props and isinstance(self.props, dict):
            map(
                lambda tup, str=start_tag: str.replace(">", f' {tup[0]}="{tup[1]}">'),
                self.props.items(),
            )

        return start_tag

    @property
    def end_tag(self):
        """end tag of hmtl string"""
        return f"</{self.tag}>"

    def set_tag(self, val):
        """Set the tag of hmtl node post initialise

        Args:
            val (str): value of tag
        """
        self.tag = val

    def set_value(self, val):
        """Set the value of hmtl node post initialise

        Args:
            val (str): value of value
        """
        self.value = val

    def to_html(self):
        """output hmtl code as string

        Raises:
            NotImplementedError: should be implented by derived classes
        """
        raise NotImplementedError()

    def props_to_html(self):
        """output prop hmtl code as string"""
        html_str = ""
        for key, val in self.props.items():
            html_str += f'<{key}> ="{val}"'
            return html_str

    def __repr__(self):
        """print overide for node repersentation"""
        return f"HTMLNode({self.tag}, {self.value}, {self.children, self.props})"
