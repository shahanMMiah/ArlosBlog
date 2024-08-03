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
        if not alts or not urls:
            raise ValueError("alt text or urls not found")

        if len(alts) != len(urls):
            raise RuntimeError("mismatch of urls and alt text found")

    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"!+\[(.*?)\]",r"\((.*?)\)"])
    return(extracter(check_func, elements))

    
def extract_markdown_links(text: str):

    def check_func(alts, urls):
        if not alts or not urls:
            raise ValueError("anchor text or urls not found")

        if len(alts) != len(urls):
            raise RuntimeError("mismatch of urls and anchor text found")

    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"\[(.*?)\]",r"\((.*?)\)"])
    return(extracter(check_func, elements))
