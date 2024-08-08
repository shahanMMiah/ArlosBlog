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