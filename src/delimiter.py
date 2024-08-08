from . import textnode
from . import markdown_utils


def split_nodes_delimiter(old_nodes: textnode.TextNode,delimiter: str,text_type: str):
        
    textNodes = []
    for old_node in old_nodes:
        if old_node.text_type != textnode.TextTypes.text_type_text.value:
            textNodes.append(old_node)
        
        else:
             splits = old_node.text.split(delimiter)
             delims_found = old_node.text.count(delimiter)

             if delims_found < 1:
                textNodes.append(old_node)
                continue
             
             elif delims_found % 2 != 0:
                 raise RuntimeError("no closing delimiter amount")
             
             for num, split in enumerate(splits):
                
                if num != len(splits) -1 and num % 2 != 0:
                    textNodes.append(
                        textnode.TextNode(
                            split,
                            text_type,
                            old_node.url,
                        )
                    )
                elif len(split) > 0:
                    textNodes.append(
                        textnode.TextNode(
                            split,
                            textnode.TextTypes.text_type_text.value,
                            old_node.url,
                        )
                    )
                """
                delim_position = 0
                delims_found = 0    
                
                for tNum, tChar in enumerate(old_node.text):
                    node_type = textnode.TextTypes.text_type_text.value
                    if tChar == delimiter:
                        
                        delims_found += 1
                        
                        if delims_found % 2 == 0:
                            node_type = text_type
                        
                        new_text = textnode.TextNode(
                                old_node.text[delim_position:tNum], 
                                node_type, old_node.url)
                        if len(new_text.text) > 1:
                            textNodes.append(new_text)
                        
                    
                        delim_position = tNum + 1
                        
                    if tNum == len(old_node.text)-1:
                    
                        end_text = textnode.TextNode(
                                old_node.text[delim_position::], 
                                node_type, old_node.url)
                        

                        if len(end_text.text) > 1:
                            textNodes.append(end_text)

                
                if delims_found < 2 or delims_found % 2 != 0:
                    raise RuntimeError("no closing delimiter amount")
                """
            
    return(textNodes)




def split_nodes_type(nodes,extract_func, text_type,split_str):

    def split_node_type(nodes_to_check,element):
        check_nodes = nodes_to_check.copy()

        for check_num, node_to_check in enumerate(nodes_to_check):
            delimiter = split_str.format(element[0],element[1])
            splits = node_to_check.text.split(delimiter)
            delim_count = node_to_check.text.count(delimiter)
            
            if delim_count == 0:
                continue
            
            check_nodes.pop(check_num)
            for num, split in enumerate(splits):
                if len(split) > 0:
                    check_nodes.append(
                        textnode.TextNode(
                            split,
                            textnode.TextTypes.text_type_text.value,
                            None,
                        )
                    )
                if num != len(splits) -1:
                    check_nodes.append(
                        textnode.TextNode(
                            element[0],
                            text_type,
                            element[1]
                        )
                    )
                          
        return(check_nodes)

    split_nodes = []

    for old_node in nodes:
        if old_node.text_type != textnode.TextTypes.text_type_text.value:
            split_nodes.append(old_node)
            continue
        
        extracted_elements = extract_func(old_node.text) 
        if not extracted_elements and old_node not in split_nodes:
            split_nodes.append(old_node)
            continue
        
        nodes_to_check = [old_node]
        for element in extracted_elements:
            nodes_to_check =split_node_type(nodes_to_check, element)
            
    
        split_nodes += nodes_to_check
        
    return(split_nodes)
                    
def split_nodes_links(nodes):
    
    return(
        split_nodes_type(
            nodes, 
            markdown_utils.extract_markdown_links, 
            textnode.TextTypes.text_type_link.value,
            "[{}]({})"
            )
        )
            
def split_nodes_images(nodes):
    
    return(
        split_nodes_type(
            nodes, 
            markdown_utils.extract_markdown_images, 
            textnode.TextTypes.text_type_image.value,
            "![{}]({})"
            )
        )
    
def text_to_textnode(text : str):
    
    text_chars = ["**","*","`",]
    text_types = [
        textnode.TextTypes.text_type_bold.value,
        textnode.TextTypes.text_type_italic.value,
        textnode.TextTypes.text_type_code.value,
    ]
    
    nodes = [textnode.TextNode(text,textnode.TextTypes.text_type_text.value,None)]
    for num, char in enumerate(text_chars):
    
        nodes = split_nodes_delimiter(nodes, char, text_types[num])
    
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    

    return(nodes)

    
            