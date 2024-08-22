from .markdown import block
import locale
import logging

LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

def extract_title_from_file(markdown_file):
    mrkdown = read_markdown(markdown_file)
    return(extract_title(mrkdown))
    
def extract_title(markdown : str):
    
    html_nodes  = block.markdown_to_hmtl_node(markdown)
    
    header_nodes = list(
        filter(
            lambda h : h.tag == "h1",
            html_nodes.children
            ))
    
    if not header_nodes:
        raise RuntimeError("no title node found")
    

    return(header_nodes[0])

    
def read_markdown(file_path):

    markdown = str()
    with open(file_path, encoding = locale.getpreferredencoding()) as file_obj:
        markdown = file_obj.read()
    return(markdown)


def generate_page(
        from_path, 
        template_path, 
        dest_path):
    
    
    LOG.info(f"generating file from {from_path}")

    from_mrkdown = read_markdown(from_path)
    from_html_nodes = block.markdown_to_hmtl_node(from_mrkdown)
    template_html = str()
    with open(template_path,  encoding = locale.getpreferredencoding()) as template_obj:
        template_html = template_obj.read()

    title_node  = extract_title(from_mrkdown)
    
    template_html = template_html.replace("{{ Title }}",title_node.value) 
    template_html = template_html.replace("{{ Content }}",from_html_nodes.to_html())

    with open(dest_path, 'w', encoding = locale.getpreferredencoding()) as dest_obj:
        
        dest_obj.write(template_html)  

    