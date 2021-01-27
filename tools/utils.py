import logging
_logger = logging.getLogger(__name__)


try:
    from html2text import HTML2Text
except ImportError as error:
    _logger.debug(error)


def html2text(html):
    """ covert html to text, ignoring images and tables
    """
    if not html:
        return ""

    ht = HTML2Text()
    ht.ignore_images = True
    ht.ignore_tables = True
    ht.ignore_emphasis = True
    ht.ignore_links = True
    return ht.handle(html)


def _get_preview_from_html(html):
    text_list = html2text(html).splitlines()
    result = []
    while len(
            result) <= 3 and text_list:
        line = text_list.pop(0)
        line = line.lstrip('#').strip()
        if not line:
            continue
        result.append(line)
    return "\n".join(result)
