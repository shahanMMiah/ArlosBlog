"""webpage module unit test"""

import os
import unittest
import logging
from src import webpage
from src.markdown import block


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


class TestWebpage(unittest.TestCase):

    def test_get_title(self):

        title = webpage.extract_title_from_file(
            os.path.join(PROJECT_DIR, "content", "index.md")
        )
        should_be = "HTMLNode(h1, None, ([HTMLNode(None, Tolkien Fan Club, (None, None))], None))"

        self.assertEqual(title.__repr__(), should_be)

        test = webpage.extract_title("# Hello")
        should_be = "HTMLNode(h1, None, ([HTMLNode(None, Hello, (None, None))], None))"

        self.assertEqual(test.__repr__(), should_be)

    def test_node_from_markdown(self):

        from_mrkdown = webpage.read_markdown(
            os.path.join(PROJECT_DIR, "content", "index.md")
        )
        from_html_nodes = block.markdown_to_hmtl_node(from_mrkdown)

        should_be = from_html_nodes.to_html()
        LOG.info("markdown converted to %s", from_html_nodes.to_html())

        self.assertEqual(from_html_nodes.to_html(), should_be)


if __name__ == "__main__":
    unittest.main()
