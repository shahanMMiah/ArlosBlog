"""inline module unit tests"""
import unittest
import logging

import src.markdown.inline as inline
import src.nodes.textnode as textnode
from src import datatypes


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Testinline(unittest.TestCase):

    def test_delimit(self):
        node = textnode.TextNode(
            "This is text with a `code block` word",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )
        new_nodes = inline.split_nodes_delimiter(
            [node], "`", datatypes.TextTypes.CODE_NAME.value
        )

        nodes_test = [
            textnode.TextNode("This is text with a ", "text", None),
            textnode.TextNode("code block", "code", None),
            textnode.TextNode(" word", "text", None),
        ]

        LOG.info(" %s should match %s", new_nodes, nodes_test)
        self.assertEqual(new_nodes, nodes_test)

    def test_multiple_text_nodes(self):
        nodes = [
            textnode.TextNode(
                "test 1 * this part is bold* line",
                datatypes.TextTypes.TEXT_NAME.value,
                None,
            ),
            textnode.TextNode(
                "test 2 **this part is bold?** line",
                datatypes.TextTypes.BOLD_NAME.value,
                None,
            ),
            textnode.TextNode(
                "test 3 * this part should be code* line",
                datatypes.TextTypes.CODE_NAME.value,
                None,
            ),
        ]

        delimit_nodes = inline.split_nodes_delimiter(
            nodes, "*", datatypes.TextTypes.BOLD_NAME.value
        )

        should_be = [
            textnode.TextNode("test 1 ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode(
                " this part is bold", datatypes.TextTypes.BOLD_NAME.value, None
            ),
            textnode.TextNode(" line", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode(
                "test 2 **this part is bold?** line",
                datatypes.TextTypes.BOLD_NAME.value,
                None,
            ),
            textnode.TextNode(
                "test 3 * this part should be code* line",
                datatypes.TextTypes.CODE_NAME.value,
                None,
            ),
        ]
        LOG.info("multiple_text_nodes looks like %s", delimit_nodes)

        self.assertEqual(delimit_nodes, should_be)

    def test_no_closing_delimiter(self):
        node = textnode.TextNode(
            "this line has no * closing delim",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )
        node2 = textnode.TextNode(
            "this line * also has* no * closing delim",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        with self.assertRaises(RuntimeError):
            inline.split_nodes_delimiter(
                [node], "*", datatypes.TextTypes.ITALIC_NAME.value
            )
            inline.split_nodes_delimiter(
                [node2], "*", datatypes.TextTypes.ITALIC_NAME.value
            )

    def test_multiple_split(self):
        node1 = textnode.TextNode(
            " this should have *multiple code* blocks * that are outputed* for this",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        delimit_nodes = inline.split_nodes_delimiter(
            [node1], "*", datatypes.TextTypes.CODE_NAME.value
        )

        should_be = [
            textnode.TextNode(
                " this should have ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "multiple code", datatypes.TextTypes.CODE_NAME.value, None
            ),
            textnode.TextNode(" blocks ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode(
                " that are outputed", datatypes.TextTypes.CODE_NAME.value, None
            ),
            textnode.TextNode(" for this", datatypes.TextTypes.TEXT_NAME.value, None),
        ]

        LOG.info("multiple split test looks like %s", delimit_nodes)

        self.assertEqual(delimit_nodes, should_be)

    def test_start_end_delimits(self):
        start_node = textnode.TextNode(
            "*this should have * a start code block",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        end_node = textnode.TextNode(
            " this should have a *end code block*",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        start_delimit = inline.split_nodes_delimiter(
            [start_node], "*", datatypes.TextTypes.CODE_NAME.value
        )
        end_delimit = inline.split_nodes_delimiter(
            [end_node], "*", datatypes.TextTypes.CODE_NAME.value
        )

        start_should_be = [
            textnode.TextNode(
                "this should have ", datatypes.TextTypes.CODE_NAME.value, None
            ),
            textnode.TextNode(
                " a start code block", datatypes.TextTypes.TEXT_NAME.value, None
            ),
        ]

        end_should_be = [
            textnode.TextNode(
                " this should have a ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "end code block", datatypes.TextTypes.CODE_NAME.value, None
            ),
        ]
 
        LOG.info("testing delimets at start %s and end %s", start_delimit, end_delimit )
        self.assertEqual(start_delimit, start_should_be)
        self.assertEqual(end_delimit, end_should_be)

    def test_split_nodes_links(self):

        node = textnode.TextNode(
            "[to boot dev](https://www.boot.dev) This is text with a link and [to youtube](https://www.youtube.com/@bootdotdev) huh",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        new_nodes = inline.split_nodes_links([node])

        should_be = [
            textnode.TextNode(
                "to boot dev",
                datatypes.TextTypes.LINK_NAME.value,
                "https://www.boot.dev",
            ),
            textnode.TextNode(
                " This is text with a link and ",
                datatypes.TextTypes.TEXT_NAME.value,
                None,
            ),
            textnode.TextNode(
                "to youtube",
                datatypes.TextTypes.LINK_NAME.value,
                "https://www.youtube.com/@bootdotdev",
            ),
            textnode.TextNode(" huh", datatypes.TextTypes.TEXT_NAME.value, None),
        ]
        LOG.info("new_nodes is %s", new_nodes)
        self.assertEqual(new_nodes, should_be)

        node2 = textnode.TextNode(
            "[to boot dev](https://www.boot.dev) This is text [with a middle link](https://www.middlelink.com) a link and [to youtube](https://www.youtube.com/@bootdotdev) huh",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )
        should_be_2 = [
            textnode.TextNode(
                "to boot dev",
                datatypes.TextTypes.LINK_NAME.value,
                "https://www.boot.dev",
            ),
            textnode.TextNode(
                " This is text ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "with a middle link",
                datatypes.TextTypes.LINK_NAME.value,
                "https://www.middlelink.com",
            ),
            textnode.TextNode(
                " a link and ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "to youtube",
                datatypes.TextTypes.LINK_NAME.value,
                "https://www.youtube.com/@bootdotdev",
            ),
            textnode.TextNode(" huh", datatypes.TextTypes.TEXT_NAME.value, None),
        ]

        new_nodes2 = inline.split_nodes_links([node2])

        self.assertEqual(new_nodes2, should_be_2)

    def test_split_images(self):

        img_node = textnode.TextNode(
            "This is a with image and ![image anchor](image_urls/images)",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        new_img_node = inline.split_nodes_images([img_node])
        img_test = [
            textnode.TextNode(
                "This is a with image and ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "image anchor",
                datatypes.TextTypes.IMAGE_NAME.value,
                "image_urls/images",
            ),
        ]
        self.assertEqual(new_img_node, img_test)

        img_node_2 = textnode.TextNode(
            "![boot img](https://www.boot.dev/img) This is a image and ![youtube logo](https://www.youtube.com/logo)",
            datatypes.TextTypes.TEXT_NAME.value,
            None,
        )

        img_new_node_2 = inline.split_nodes_images([img_node_2])

        should_be_2 = [
            textnode.TextNode(
                "boot img",
                datatypes.TextTypes.IMAGE_NAME.value,
                "https://www.boot.dev/img",
            ),
            textnode.TextNode(
                " This is a image and ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode(
                "youtube logo",
                datatypes.TextTypes.IMAGE_NAME.value,
                "https://www.youtube.com/logo",
            ),
        ]
        LOG.info("img list is %s", img_new_node_2)
        self.assertEqual(img_new_node_2, should_be_2)

    def test_text_to_textnodes(self):
        text_str = "This is **text** with an *italic* word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

        text_nodes = inline.text_to_textnode(text_str)

        should_be = [
            textnode.TextNode("This is ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode("text", datatypes.TextTypes.BOLD_NAME.value, None),
            textnode.TextNode(" with an ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode("italic", datatypes.TextTypes.ITALIC_NAME.value, None),
            textnode.TextNode(
                " word and a ", datatypes.TextTypes.TEXT_NAME.value, None
            ),
            textnode.TextNode("code block", datatypes.TextTypes.CODE_NAME.value, None),
            textnode.TextNode(" and an ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode(
                "obi wan image",
                datatypes.TextTypes.IMAGE_NAME.value,
                "https://i.imgur.com/fJRm4Vk.jpeg",
            ),
            textnode.TextNode(" and a ", datatypes.TextTypes.TEXT_NAME.value, None),
            textnode.TextNode(
                "link", datatypes.TextTypes.LINK_NAME.value, "https://boot.dev"
            ),
        ]
        LOG.info("text to textnodes is %s", text_nodes)
        self.assertEqual(text_nodes, should_be)

    def test_extract_images(self):

        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"

        extracted_images = inline.extract_markdown_images(text)

        should_be = [
            ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
            ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]

        self.assertEqual(extracted_images, should_be)

    def test_extract_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"

        extracted_links = inline.extract_markdown_links(text)

        should_be = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertEqual(extracted_links, should_be)


if __name__ == "__main__":
    unittest.main()
