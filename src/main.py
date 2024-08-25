"""main module for static site generator"""

import os
import shutil
import logging
from . import webpage

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))

LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def copy_static_content(static="static",public="public"):
    """copy content from static folder to public"""

    base_dir = os.path.dirname(os.path.dirname(__file__))
    src_dir = os.path.join(base_dir, static)
    dst_dir = os.path.join(base_dir, public)

    if os.path.exists(dst_dir):
        LOG.info("found %s re copying from %s",dst_dir,src_dir)
        shutil.rmtree(dst_dir)

    os.mkdir(dst_dir)
    copy_src_dir(src_dir, dst_dir)


def copy_src_dir(src_dir, dst_dir):
    """copy file from source dir to dst dir

    Args:
        src_dir (str): filepath to src file
        dst_dir (str): filepath to dst file
    """

    def add_file_dir(files):
        """curried function to copy dir/file to dst dir

        Args:
            files (str): filepath of file
        """
        src_file = os.path.join(src_dir, files)
        dst_file = os.path.join(dst_dir, files)
        if os.path.isdir(src_file):

            LOG.info("copying dir %s",files)

            os.mkdir(dst_file)

            copy_src_dir(
                src_file,
                dst_file,
            )

        elif os.path.isfile(src_file):
            LOG.info("copying file %s", src_file)

            shutil.copy(src_file, dst_file)

    LOG.info("copying files in %s", src_dir)

    for src in os.listdir(src_dir):

        add_file_dir(src)


def main():
    """main function to generate hmtl pages"""

    LOG.info("re copying static content")
    copy_static_content()

    webpage.generate_pages_recursive(
        os.path.join(PROJECT_DIR,"content"),
        os.path.join(PROJECT_DIR,"template.html"),
        os.path.join(PROJECT_DIR,"public")
    )


if __name__ == "__main__":
    main()
