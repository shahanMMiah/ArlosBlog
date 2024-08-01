from . import textnode

def split_nodes_delimiter(old_nodes: textnode.TextNode,delimiter: str,text_type: str):
    textNodes = []
    for old_node in old_nodes:
        if old_node.text_type != textnode.TextTypes.text_type_text.value:
            text_type.append(textNodes)
        
        else:
            delim_position = 0
            delims_found = 0    
            
            for tNum, tChar in enumerate(old_node.text):
                node_type = textnode.TextTypes.text_type_text.value
                if tChar == delimiter:
                    
                    delims_found += 1
                    
                    if delims_found % 2 == 0:
                        node_type = text_type
                    
                    textNodes.append(
                        textnode.TextNode(
                            old_node.text[delim_position:tNum], 
                            node_type, old_node.url)
                    )
                
                    delim_position = tNum + 1
                    
                if tNum == len(old_node.text)-1:
                    textNodes.append(
                        textnode.TextNode(
                            old_node.text[delim_position::], 
                            node_type, old_node.url)
                    )

            
            if delims_found < 2 or delims_found % 2 != 0:
                raise RuntimeError("no closing delimiter amount")
            
            return(textNodes)


node = textnode.TextNode("This is text with a `code block` word", textnode.TextTypes.text_type_text.value, None)
new_nodes = split_nodes_delimiter([node], "`", textnode.TextTypes.text_type_code.value)

print(new_nodes)
    
