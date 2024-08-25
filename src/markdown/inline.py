""" inline functions for converting text string into typed text nodes
"""

import re
from .. import datatypes
from ..nodes import textnode


def extract_markdown_element(text: str):
    """extract element of text given an search pattern

    Args:
        text (str): sentence text
    """

    def find_patterns(re_patterns: list):
        """higher ord functoin for finding patterns with regex

        Args:
            re_patterns (list): list of found elements from regex pattern
        """
        return list(
            map(lambda pattern, text=text: re.findall(pattern, text), re_patterns)
        )

    def extract_element(check_func, elements):
        """extract the elements from text using pattern

        Args:
            check_func (func): patttern check function
            elements (list): list of found patterns
        Return (list): of extracted elements found
        """

        if not elements[0] or not elements[1]:
            return None

        check_func(elements[0], elements[1])

        return list(
            map(lambda num, e=elements: (e[0][num], e[1][num]), range(len(elements[0])))
        )

    return (find_patterns, extract_element)


def extract_markdown_images(text: str):
    """extract image element from text

    Args:
        text (str): sentence text
    """

    def check_func(alts, urls):
        if not alts or not urls or len(alts) != len(urls):
            return None

    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"!+\[(.*?)\]", r"\((.*?)\)"])

    return extracter(check_func, elements)


def extract_markdown_links(text: str):
    """extract link element from text

    Args:
        text (str): sentence text
    """

    def check_func(alts, urls):
        if not alts or not urls or len(alts) != len(urls):
            return None

    pattern_finder, extracter = extract_markdown_element(text)
    elements = pattern_finder([r"\[(.*?)\]", r"\((.*?)\)"])
    return extracter(check_func, elements)


def split_nodes_delimiter(old_nodes: textnode.TextNode, delimiter: str, text_type: str):
    """return elements of text as a typed text node given text type and delimeter string

    Args:
        old_nodes (textnode.TextNode): textnodes to check
        delimiter (str): string of splitting delimiter
        text_type (str): type of textnode to return

    Raises:
        RuntimeError: no closing amount of delimiters found in text
    """

    textnodes = []
    for old_node in old_nodes:
        if old_node.text_type != datatypes.TextTypes.TEXT_NAME.value:
            textnodes.append(old_node)

        else:
            splits = old_node.text.split(delimiter)
            delims_found = old_node.text.count(delimiter)

            if delims_found < 1:
                textnodes.append(old_node)
                continue

            elif delims_found % 2 != 0:
                raise RuntimeError(
                    f"no closing delimiter{delimiter} of amount {delims_found} in {old_node.text}"
                )

            for num, split in enumerate(splits):

                if num != len(splits) - 1 and num % 2 != 0 and len(split) > 0:
                    textnodes.append(
                        textnode.TextNode(
                            split,
                            text_type,
                            old_node.url,
                        )
                    )
                elif len(split) > 0:
                    textnodes.append(
                        textnode.TextNode(
                            split,
                            datatypes.TextTypes.TEXT_NAME.value,
                            old_node.url,
                        )
                    )

    return textnodes


def split_nodes_type(nodes, extract_func, text_type, split_str):
    """extract and return specified type of inline text types from textnodes

    Args:
        nodes (_type_): textnodes to check
        extract_func (_type_): type extraction method
        text_type (_type_): text type to return
        split_str (_type_): delimeter str to check in texts
    """

    def split_node_type(nodes_to_check, element):
        check_nodes = nodes_to_check.copy()

        for check_num, node_to_check in enumerate(nodes_to_check):
            delimiter = split_str.format(element[0], element[1])
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
                if num != len(splits) - 1:
                    check_nodes.append(
                        textnode.TextNode(element[0], text_type, element[1])
                    )

        return check_nodes

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
            nodes_to_check = split_node_type(nodes_to_check, element)

        split_nodes += nodes_to_check

    return split_nodes


def split_nodes_links(nodes):
    """find and return inline link textnodes

    Args:
        nodes (list): list of nodes to check
    """

    return split_nodes_type(
        nodes, extract_markdown_links, datatypes.TextTypes.LINK_NAME.value, "[{}]({})"
    )


def split_nodes_images(nodes):
    """find and return inline image textnodes

    Args:
        nodes (list): list of nodes to check
    """

    return split_nodes_type(
        nodes,
        extract_markdown_images,
        datatypes.TextTypes.IMAGE_NAME.value,
        "![{}]({})",
    )


def text_to_textnode(text: str):
    """check for predifned text types and return inline type texnodes

    Args:
        text (str): sentence text
    """

    text_chars = [
        datatypes.InlineTypes.BOLD.value,
        datatypes.InlineTypes.ITALIC.value,
        datatypes.InlineTypes.CODE.value,
    ]
    text_types = [
        datatypes.TextTypes.BOLD_NAME.value,
        datatypes.TextTypes.ITALIC_NAME.value,
        datatypes.TextTypes.CODE_NAME.value,
    ]

    nodes = [textnode.TextNode(text, datatypes.TextTypes.TEXT_NAME.value, None)]

    for num, char in enumerate(text_chars):

        nodes = split_nodes_delimiter(nodes, char, text_types[num])

    nodes = split_nodes_images(nodes)
    nodes = split_nodes_links(nodes)

    return nodes
