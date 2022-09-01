"""Markdown Processing.

This module contains the methods responsible for blag's markdown
processing.

"""

# remove when we don't support py38 anymore
from __future__ import annotations
from datetime import datetime
import logging
from urllib.parse import urlsplit, urlunsplit
from xml.etree.ElementTree import Element

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor


logger = logging.getLogger(__name__)


def markdown_factory() -> Markdown:
    """Create a Markdown instance.

    This method exists only to ensure we use the same Markdown instance
    for tests as for the actual thing.

    Returns
    -------
    markdown.Markdown

    """
    md = Markdown(
        extensions=[
            'meta',
            'fenced_code',
            'codehilite',
            'smarty',
            MarkdownLinkExtension(),
        ],
        output_format='html',
    )
    return md


def convert_markdown(
    md: Markdown,
    markdown: str,
) -> tuple[str, dict[str, str]]:
    """Convert markdown into html and extract meta data.

    Some meta data is treated special:
        * `date` is converted into datetime with local timezone
        * `tags` is interpreted as a comma-separeted list of strings.
          All strings are stripped and converted to lower case.

    Parameters
    ----------
    md
        the Markdown instance
    markdown
        the markdown text that should be converted

    Returns
    -------
    str, dict[str, str]
        html and metadata

    """
    md.reset()
    content = md.convert(markdown)
    meta = md.Meta  # type: ignore

    # markdowns metadata consists as list of strings -- one item per
    # line. let's convert into single strings.
    for key, value in meta.items():
        value = '\n'.join(value)
        meta[key] = value

    # convert known metadata
    # date: datetime
    if 'date' in meta:
        meta['date'] = datetime.fromisoformat(meta['date'])
        meta['date'] = meta['date'].astimezone()
    # tags: list[str] and lower case
    if 'tags' in meta:
        tags = meta['tags'].split(',')
        tags = [t.lower() for t in tags]
        tags = [t.strip() for t in tags]
        meta['tags'] = tags

    return content, meta


class MarkdownLinkTreeprocessor(Treeprocessor):
    """Converts relative links to .md files to .html"""

    def run(self, root: Element) -> Element:
        for element in root.iter():
            if element.tag == 'a':
                url = element.get('href')
                # element.get could also return None, we haven't seen this so
                # far, so lets wait if we raise this
                assert url is not None
                url = str(url)
                converted = self.convert(url)
                element.set('href', converted)
        return root

    def convert(self, url: str) -> str:
        scheme, netloc, path, query, fragment = urlsplit(url)
        logger.debug(
            f'{url}: {scheme=} {netloc=} {path=} {query=} {fragment=}'
        )
        if scheme or netloc or not path:
            return url
        if path.endswith('.md'):
            path = path[:-3] + '.html'

        url = urlunsplit((scheme, netloc, path, query, fragment))
        return url


class MarkdownLinkExtension(Extension):
    """markdown.extension that converts relative .md- to .html-links."""

    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(
            MarkdownLinkTreeprocessor(md),
            'mdlink',
            0,
        )
