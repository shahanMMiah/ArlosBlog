import re
from enum import Enum

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


def markdown_to_blocks(markdown : str):

    splits = markdown.split("\n")
    sentences = []
    current_sentence = str()
    for num, sentence in enumerate(splits):
        
        if not sentence and current_sentence or num == len(splits)-1:
            sentences.append(current_sentence)
            current_sentence = str()
        else:
            add_sent = sentence.lstrip(' ').rstrip(' ')
            if len(current_sentence) > 0:
                add_sent = f"\n{add_sent}"
            current_sentence += add_sent
    return(sentences)

### block funcs #### 
class BlockTypes(Enum):
    HEADING = "#"
    CODE = "```"
    QOUTE = ">"
    UNORDERED_LIST = ["*","-"]
    ORDERED_LIST = "."
       
    HEADING_NAME = "heading"
    CODE_NAME = "code"
    QOUTE_NAME = "qoute"
    UNORDERED_NAME = "unordered_list"
    ORDERED_NAME = "ordered_list"
    PARAGRAPH_NAME = "paragraph"

    @classmethod
    def heading_check(self, block:str):
        if block.startswith(BlockTypes.HEADING.value):
            hash_count = block.count(BlockTypes.HEADING.value)
            if hash_count > 0 and hash_count <= 6:
                return(BlockTypes.HEADING_NAME.value)
        
        return(block)
    @classmethod
    def code_check(self, block:str):
        if block.startswith(f"{BlockTypes.CODE.value} "):
            return(BlockTypes.CODE_NAME.value)
        return(block)
    
    @classmethod
    def quote_check(self, block:str):
        if block.startswith(f"{BlockTypes.QOUTE.value} "):
            return(BlockTypes.QOUTE_NAME.value)
        return(block)
    
    @classmethod
    def unordered_list_check(self, block:str):
        if block.startswith(
            f"{BlockTypes.UNORDERED_LIST.value[0]} "):
        
            return(BlockTypes.UNORDERED_NAME.value)
        
        elif block.startswith(
                f"{BlockTypes.UNORDERED_LIST.value[1]} "):
            return(BlockTypes.UNORDERED_NAME.value)
        else:
            return(block)
    
    @classmethod
    def ordered_list_check(self, block:str):
        lines = block.split("\n")
        ord_num = 0
        

        for line in lines:
            if line:
                if line[0].isnumeric() and line[1] == "." and int(line[0]) == ord_num +1:
                    ord_num += 1
                else:
                    return(block)
                    
        return(BlockTypes.ORDERED_NAME.value)
        


def block_to_block_type(block : str):

    type_ls = [BlockTypes.heading_check,
               BlockTypes.code_check,
               BlockTypes.quote_check,
               BlockTypes.unordered_list_check,
               BlockTypes.ordered_list_check,
               ]
    for type_func in type_ls:
        checked_block = type_func(block)

        if checked_block != block:
            return(checked_block)
            
    return(BlockTypes.PARAGRAPH_NAME.value)
    


    
    

        
        

