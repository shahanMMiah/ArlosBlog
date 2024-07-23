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
    
def main():

    text_node = TextNode("This is a text node", "bold", "https://www.boot.dev")
    print(text_node)