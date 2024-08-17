import os
import shutil
import logging



LOG = logging.getLogger(__name__)
logging.basicConfig(level = logging.INFO)

def copy_static_content():

    base_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(base_dir,"static")
    dst_dir = os.path.join(base_dir,"public")
    
    if os.path.exists(dst_dir):
        LOG.info(f"found {dst_dir} re copying from {src_dir}")
        shutil.rmtree(dst_dir)

    os.mkdir(dst_dir)
    copy_src_dir(src_dir, dst_dir)
     

def copy_src_dir(src_dir,dst_dir):
    
    def add_file_dir(files):
        src_file = os.path.join(src_dir,files)
        dst_file=  os.path.join(dst_dir,files)
        if os.path.isdir(src_file):

            LOG.info(f"copying dir {files}")
            
            os.mkdir(dst_file)
            
            copy_src_dir(
                src_file, 
                dst_file, 
            )
        
        elif os.path.isfile(src_file):
            LOG.info(f"copying file {files}")
        
            shutil.copy(src_file,dst_file)
        

    LOG.info(f"copying files in {src_dir}")
    
    for src in os.listdir(src_dir):
    
        add_file_dir(src)
        

        
def main():        
    copy_static_content()

if __name__ == "__main__":
    main()

    


                