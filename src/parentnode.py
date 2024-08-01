from .htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self,  tag=None, children=None, props=None):
        assert(children is not None)
        super(ParentNode, self).__init__(
            children=children,
            tag=tag,
            value=None,
            props=props
        )
    def to_html(self, output_str = ""):
 
        output_str += self.start_tag

        if not self.tag:
            raise ValueError(f"{self.__repr__()} has no tag")
        if not self.children:
             raise ValueError(f"{self.__repr__()} has no children")

        for childs in self.children:
            if isinstance(childs, ParentNode):
                output_str = childs.to_html(
                    output_str=output_str)
            else:
                output_str += childs.to_html()
            
        output_str+= self.end_tag                    
        
        return(output_str)
    

        
