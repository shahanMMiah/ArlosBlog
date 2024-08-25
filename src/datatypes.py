""" data module for common shared enum types """

from enum import Enum


class BlockTypes(Enum):
    """shared block type enums

    Args:
        Enum (Enum): enum class
    """

    HEADING = "#"
    CODE = "`"
    QOUTE = ">"
    UNORDERED_LIST = ["*", "-"]
    ORDERED_LIST = "."

    HEADING_NAME = "heading"
    CODE_NAME = "code"
    QOUTE_NAME = "qoute"
    UNORDERED_NAME = "unordered_list"
    ORDERED_NAME = "ordered_list"
    PARAGRAPH_NAME = "paragraph"

    HEADING_TAG = "h"
    PARAGRAPH_TAG = "p"
    UNORDERED_LIST_TAG = ["ul", "li"]
    ORDERED_LIST_TAG = ["ol", "li"]
    QOUTE_TAG = "blockquote"
    CODE_TAG = "code"

    PREFORMAT_TAG = "pre"
    CONETNT_TAG = "div"


class InlineTypes(Enum):
    """shared inline type enums

    Args:
        Enum (Enum): enum class
    """

    BOLD_TAG = "b"
    ITALIC_TAG = "i"
    LINK_TAG = "a"
    IMAGE_TAG = "img"

    BOLD = "**"
    ITALIC = "*"
    CODE = "`"


class TextTypes(Enum):
    """shared text type enums

    Args:
        Enum (Enum): enum class
    """

    TEXT_NAME = "text"
    BOLD_NAME = "bold"
    ITALIC_NAME = "italic"
    CODE_NAME = "code"
    LINK_NAME = "link"
    IMAGE_NAME = "image"
    NULL_NAME = "null"
