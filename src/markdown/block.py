""" block functions for converting markdown blocks into hmtl nodes
"""

import re
import functools
from ..nodes import parentnode, textnode
from .. import datatypes
from . import inline


# check funcs
def heading_check(block: str):
    """Check if block is heading type

    Args:
        block (str): markdown string block
    """
    if block.startswith(datatypes.BlockTypes.HEADING.value):
        hash_count = block.count(datatypes.BlockTypes.HEADING.value)
        if hash_count > 0 and hash_count <= 6:
            return datatypes.BlockTypes.HEADING_NAME.value

    return block


def code_check(block: str):
    """Check if block is code type

    Args:
        block (str): markdown string block
    """
    if block.startswith(f"{datatypes.BlockTypes.CODE.value}"):
        return datatypes.BlockTypes.CODE_NAME.value
    return block


def quote_check(block: str):
    """Check if block is qoute type

    Args:
        block (str): markdown string block
    """
    if block.startswith(f"{datatypes.BlockTypes.QOUTE.value} "):
        return datatypes.BlockTypes.QOUTE_NAME.value
    return block


def unordered_list_check(block: str):
    """Check if block is unordered_list type

    Args:
        block (str): markdown string block
    """
    if block.startswith(f"{datatypes.BlockTypes.UNORDERED_LIST.value[0]} "):

        return datatypes.BlockTypes.UNORDERED_NAME.value

    elif block.startswith(f"{datatypes.BlockTypes.UNORDERED_LIST.value[1]} "):
        return datatypes.BlockTypes.UNORDERED_NAME.value
    else:
        return block


def ordered_list_check(block: str):
    """Check if block is ordered_list type

    Args:
        block (str): markdown string block
    """

    lines = block.split("\n")
    ord_num = 0

    for line in lines:
        if line:
            if line[0].isnumeric() and line[1] == "." and int(line[0]) == ord_num + 1:
                ord_num += 1
            else:
                return block

    return datatypes.BlockTypes.ORDERED_NAME.value


def markdown_to_blocks(markdown: str):
    """spllit markdown string into a list of blocks

    Args:
        block (str): markdown content as string
    """

    delims_types = [
        datatypes.InlineTypes.BOLD.value,
        datatypes.InlineTypes.ITALIC.value,
        datatypes.InlineTypes.CODE.value,
    ]

    splits = markdown.split("\n")
    sentences = []
    current_sentence = str()
    for num, sentence in enumerate(splits):
        add_sent = sentence.lstrip(" ").rstrip(" ")

        if num == len(splits) - 1:
            current_sentence += add_sent
            sentences.append(current_sentence)

        elif not sentence and current_sentence:
            sentences.append(current_sentence)
            current_sentence = str()
        else:
            if len(current_sentence) > 0 and not add_sent in delims_types:
                add_sent = f"\n{add_sent}"
            current_sentence += add_sent

    return sentences


def block_to_block_type(block: str):
    """return the type of a markdown block

    Args:
        block (str): markdown block content as string
    """

    type_ls = [
        heading_check,
        code_check,
        quote_check,
        unordered_list_check,
        ordered_list_check,
    ]

    for type_func in type_ls:

        checked_block = type_func(block)

        if checked_block != block:
            return checked_block

    return datatypes.BlockTypes.PARAGRAPH_NAME.value


def markdown_to_hmtl_node(markdown: str):
    """convert markdown block into a hmtl node

    Args:
        block (str): markdown content as string
    """

    block_func_dict = {
        datatypes.BlockTypes.HEADING_NAME.value: block_to_heading_node,
        datatypes.BlockTypes.UNORDERED_NAME.value: block_to_unordered_list_node,
        datatypes.BlockTypes.ORDERED_NAME.value: block_to_ordered_list_node,
        datatypes.BlockTypes.QOUTE_NAME.value: block_to_quoute_node,
        datatypes.BlockTypes.CODE_NAME.value: block_to_code_node,
        datatypes.BlockTypes.PARAGRAPH_NAME.value: block_to_paragraphs_node,
    }

    return parentnode.ParentNode(
        datatypes.BlockTypes.CONETNT_TAG.value,
        list(
            map(
                lambda block: block_func_dict[block_to_block_type(block)](block),
                markdown_to_blocks(markdown),
            )
        ),
        None,
    )


def text_to_children(text: str):
    """return list of textnodes converted from text string

    Args:
        text (str): text of a block
    """

    text_split = list(filter(lambda txt: txt != "", text.split("\n")))

    if (
        not text_split
        or block_to_block_type(text) == datatypes.BlockTypes.CODE_NAME.value
    ):
        text_split = [text]

    text_nodes = functools.reduce(
        lambda text_nodes, txt: text_nodes + inline.text_to_textnode(txt),
        text_split,
        [],
    )

    return list(map(textnode.text_to_html_node, text_nodes))


def block_to_heading_node(block: str):
    """converts heading type block string into hmtl nodes

    Args:
        block (str): block content as string
    """

    hash_count = block.count(datatypes.BlockTypes.HEADING.value)

    return parentnode.ParentNode(
        f"{datatypes.BlockTypes.HEADING_TAG.value}{hash_count}",
        text_to_children(
            block.strip(datatypes.BlockTypes.HEADING.value).lstrip(" ").rstrip(" ")
        ),
        None,
    )


def block_to_unordered_list_node(block: str):
    """converts unordered list type block string into hmtl nodes

    Args:
        block (str): block content as string
    """

    text_split = block.split("\n")

    node_list = []
    for text in text_split:
        strip_text = (
            text.lstrip(datatypes.BlockTypes.UNORDERED_LIST.value[0])
            .lstrip(datatypes.BlockTypes.UNORDERED_LIST.value[1])
            .lstrip(" ")
            .rstrip(" ")
        )
        child_nodes = text_to_children(strip_text)

        child_nodes = parentnode.ParentNode(
            datatypes.TextTypes.NULL_NAME.value, child_nodes, None
        )

        child_nodes.set_tag(datatypes.BlockTypes.UNORDERED_LIST_TAG.value[1])
        node_list.append(child_nodes)

    return parentnode.ParentNode(
        datatypes.BlockTypes.UNORDERED_LIST_TAG.value[0], node_list, None
    )


def block_to_ordered_list_node(block: str):
    """converts ordered list type block string into hmtl nodes

    Args:
        block (str): block content as string
    """

    nums = re.findall(r"\d.", block)

    strip_block = block.split("\n")

    node_list = []
    for text in strip_block:

        if not text:
            continue

        un_num = text
        for num in nums:
            if num in text:
                un_num = text.replace(num, "")

        child_nodes = text_to_children(un_num)
        for child in child_nodes:

            striped = child.value.lstrip(" ")
            child.set_value(striped)

        if len(child_nodes) > 1:
            child_nodes = parentnode.ParentNode(
                datatypes.TextTypes.NULL_NAME.value, child_nodes, None
            )

        else:
            child_nodes = child_nodes[0]

        child_nodes.set_tag(datatypes.BlockTypes.ORDERED_LIST_TAG.value[1])
        node_list.append(child_nodes)

    return parentnode.ParentNode(
        datatypes.BlockTypes.ORDERED_LIST_TAG.value[0], node_list, None
    )


def block_to_quoute_node(block: str):
    """converts qoute type block string into hmtl nodes

    Args:
        block (str): block content as string
    """

    striped_block = block.replace(datatypes.BlockTypes.QOUTE.value, "")

    return parentnode.ParentNode(
        datatypes.BlockTypes.QOUTE_TAG.value,
        text_to_children(striped_block.lstrip(" ").rstrip(" ")),
        None,
    )


def block_to_code_node(block: str):
    """converts code type block string into hmtl

    Args:
        block (str): block content as string
    """

    return parentnode.ParentNode(
        datatypes.BlockTypes.PREFORMAT_TAG.value, text_to_children(block), None
    )


def block_to_paragraphs_node(block: str):
    """converts paragraph type block string into hmtl

    Args:
        block (str): block content as string
    """

    return parentnode.ParentNode(
        datatypes.BlockTypes.PARAGRAPH_TAG.value, text_to_children(block), None
    )
