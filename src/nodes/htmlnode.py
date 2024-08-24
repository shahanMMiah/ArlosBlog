    
class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    @property
    def start_tag(self):
        start_tag  = f"<{self.tag}>"
        if self.props and isinstance(self.props, dict):
            map(
                lambda tup, str = start_tag : str.replace(
                    '>', 
                    f' {tup[0]}="{tup[1]}">'),
                self.props.items()
                )
            
        return(start_tag)
    
    @property
    def end_tag(self):
        return(f"</{self.tag}>")

    def set_tag(self, val):
        self.tag = val

    def set_value(self, val):
        self.value = val
        
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        html_str = ''
        for key,val in self.props.items():
            html_str += f'<{key}> ="{val}"'  
        return(html_str)
    
    def __repr__(self):
        return(
            f"HTMLNode({self.tag}, {self.value}, {self.children, self.props})"
            )