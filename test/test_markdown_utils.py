import unittest

import src.markdown_utils as mk_utils

class TestMarkdownUtils(unittest.TestCase):
    
    def test_extract_images(self):
        
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
 
        extracted_images = mk_utils.extract_markdown_images(text)

        should_be = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

        self.assertEqual(extracted_images, should_be)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        
        extracted_links = mk_utils.extract_markdown_links(text)

        should_be = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

        self.assertEqual(extracted_links, should_be)

    def test_no_found_match(self):
        link_test = "This is text with a link [to boot dev] this should break"

        with self.assertRaises(ValueError):
            mk_utils.extract_markdown_links(link_test)

    def test_mismatch_url_found(self):
        link_test = "This is text with a link [to boot dev] [this is too many anchors](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        with self.assertRaises(RuntimeError):
            mk_utils.extract_markdown_links(link_test)
        

if __name__ == "__main__":
    unittest.main()