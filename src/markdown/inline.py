from .. import datatypes
from ..nodes import textnode
import re


def extract_markdown_element(text:str):
    
    def find_patterns(re_patterns : list):
        return(
            list(map(
                lambda pattern, text = text : re.findall(
                    pattern, text), re_patterns)
                    )
            )
 
    def extract_element(check_func, elements):
        
        check_func(elements[0],elements[1])
       
        return(
            list( map(lambda num, e=elements : (e[0][num],e[1][num]), range(len(elements[0]))))
        )
        
    return(find_patterns,extract_element)

def extract_markdown_images(text : str):

    def check_func(alts, urls):
        if not alts or not urls or len(alts) != len(urls):
            return None


    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"!+\[(.*?)\]",r"\((.*?)\)"])
    return(extracter(check_func, elements))

    
def extract_markdown_links(text: str):

    def check_func(alts, urls):
        if not alts or not urls or len(alts) != len(urls):
            return None

    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"\[(.*?)\]",r"\((.*?)\)"])
    return(extracter(check_func, elements))


def split_nodes_delimiter(old_nodes: textnode.TextNode,delimiter: str,text_type: str):
        
    textNodes = []
    for old_node in old_nodes:
        if old_node.text_type != datatypes.TextTypes.TEXT_NAME.value:
            textNodes.append(old_node)
        
        else:
             splits = old_node.text.split(delimiter)
             delims_found = old_node.text.count(delimiter)

             if delims_found < 1:
                textNodes.append(old_node)
                continue
             
             elif delims_found % 2 != 0:
                 raise RuntimeError(f"no closing delimiter{delimiter} of amount {delims_found} in {old_node.text}")
             
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
                            datatypes.TextTypes.TEXT_NAME.value,
                            old_node.url,
                        )
                    )

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
                            datatypes.TextTypes.TEXT_NAME.value,
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
        if old_node.text_type != datatypes.TextTypes.TEXT_NAME.value:
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
            extract_markdown_links, 
            datatypes.TextTypes.LINK_NAME.value,
            "[{}]({})"
            )
        )
            
def split_nodes_images(nodes):
    
    return(
        split_nodes_type(
            nodes, 
            extract_markdown_images, 
            datatypes.TextTypes.IMAGE_NAME.value,
            "![{}]({})"
            )
        )
    
def text_to_textnode(text : str):
    
    text_chars = [
        datatypes.InlineTypes.BOLD.value,
        datatypes.InlineTypes.ITALIC.value,
        datatypes.InlineTypes.CODE.value
    ]
    text_types = [
        datatypes.TextTypes.BOLD_NAME.value,
        datatypes.TextTypes.ITALIC_NAME.value,
        datatypes.TextTypes.CODE_NAME.value,
    ]
    
    nodes = [textnode.TextNode(text,datatypes.TextTypes.TEXT_NAME.value,None)]
    for num, char in enumerate(text_chars):
    
        nodes = split_nodes_delimiter(nodes, char, text_types[num])
    
    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)
    

    return(nodes)

    
            