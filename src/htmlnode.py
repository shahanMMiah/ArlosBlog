
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

        self.tag_dict = {
            "p":"p>", "a":"a "}

    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_str = ''
        for key,val in self.props.items():
            html_str += f' <{key}> ="{val}"'  
        return(html_str)
    
    def __repr__(self):
        return(
            f"HTMLNode({self.tag}, {self.value}, {self.children, self.props})"
            )