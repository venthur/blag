#!/usr/bin/env python

"""Small static site generator.

"""


__author__ = "Bastian Venthur <venthur@debian.org>"


import argparse
import os
import shutil
import logging
from datetime import datetime
from urllib.parse import urlsplit, urlunsplit

from markdown import Markdown
from markdown.extensions import Extension
from markdown.treeprocessors import Treeprocessor
from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader
import feedgenerator

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
)


def main(args=None):
    args = parse_args(args)
    args.func(args)


def parse_args(args):
    """Parse command line arguments.

    Paramters
    ---------
    args :
        optional parameters, used for testing

    Returns
    -------
    args

    """
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    build_parser = commands.add_parser('build')
    build_parser.set_defaults(func=build)
    build_parser.add_argument(
            '-i', '--input-dir',
            default='content',
            help='Input directory (default: content)',
    )
    build_parser.add_argument(
            '-o', '--output-dir',
            default='build',
            help='Ouptut directory (default: build)',
    )

    return parser.parse_args()


def build(args):
    os.makedirs(f'{args.output_dir}', exist_ok=True)
    convertibles = []
    for root, dirnames, filenames in os.walk(args.input_dir):
        for filename in filenames:
            rel_src = os.path.relpath(f'{root}/{filename}', start=args.input_dir)
            # all non-markdown files are just copied over, the markdown
            # files are converted to html
            if rel_src.endswith('.md'):
                rel_dst = rel_src
                rel_dst = rel_dst[:-3] + '.html'
                convertibles.append((rel_src, rel_dst))
            else:
                shutil.copy(f'{args.input_dir}/{rel_src}', f'{args.output_dir}/{rel_src}')
        for dirname in dirnames:
            # all directories are copied into the output directory
            path = os.path.relpath(f'{root}/{dirname}', start=args.input_dir)
            os.makedirs(f'{args.output_dir}/{path}', exist_ok=True)

    convert_to_html(convertibles, args.input_dir, args.output_dir)


def markdown_factory():
    """Create a Markdown instance.

    This method exists only to ensure we use the same Markdown instance
    for tests as for the actual thing.

    Returns
    -------
    markdown.Markdown

    """
    md = Markdown(
        extensions=[
            'meta', 'fenced_code', 'codehilite',
            MarkdownLinkExtension()
        ],
        output_format='html5',
    )
    return md


def convert_to_html(convertibles, input_dir, output_dir):

    env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader(['templates']),
                PackageLoader('sg', 'templates'),
            ])
    )

    md = markdown_factory()

    articles = []

    for src, dst in convertibles:
        logger.debug(f'Processing {src}')
        with open(f'{input_dir}/{src}', 'r') as fh:
            body = fh.read()

        content, meta = convert_markdown(md, body)

        context = dict(content=content)
        context.update(meta)

        if meta and 'date' in meta:
            articles.append((dst, context))
        template = env.get_template('article.html')
        result = template.render(context)
        with open(f'{output_dir}/{dst}', 'w') as fh_dest:
            fh_dest.write(result)

    # generate feed
    feed = feedgenerator.Atom1Feed(
            link='https://venthur.de',
            title='my title',
            description='basti"s blag',
    )

    for dst, context in articles:
        feed.add_item(
            title=context['title'],
            link=dst,
            description=context['title'],
            content=context['content'],
            pubdate=context['date'],
        )

    with open('atom.xml', 'w') as fh:
        feed.write(fh, encoding='utf8')

    # generate archive
    ctx = {}
    archive = []
    for dst, context in articles:
        entry = context.copy()
        entry['dst'] = dst
        archive.append(entry)
    archive = sorted(archive, key=lambda x: x['date'], reverse=True)
    ctx['archive'] = archive
    template = env.get_template('archive.html')
    result = template.render(ctx)
    with open('build/index.html', 'w') as fh:
        fh.write(result)

    ## generate tags
    #ctx = {}
    #tags = {}
    #for dst, context in articles:
    #    logger.debug(f'{dst}: {context}')
    #    entry = context.copy()
    #    entry['dst'] = dst
    #    for tag in context['tags']:
    #        tags['tag'] = tags.get(tag, []).append(entry)
    #tags = list(tags)
    #tags = sorted(tags)
    #ctx['tags'] = tags
    #template = env.get_template('tags.html')
    #result = template.render(ctx)
    #with open('tags.html', 'w') as fh:
    #    fh.write(result)



def convert_markdown(md, markdown):
    """Convert markdown into html and extract meta data.

    Parameters
    ----------
    md : markdown.Markdown instance
    markdown : str

    Returns
    -------
    str, dict :
        html and metadata

    """
    md.reset()
    content = md.convert(markdown)
    meta = md.Meta

    # markdowns metadata consists as list of strings -- one item per
    # line. let's convert into single strings.
    for key, value in meta.items():
        value = '\n'.join(value)
        meta[key] = value

    # convert known metadata
    # date: datetime
    if 'date' in meta:
        meta['date'] = datetime.fromisoformat(meta['date'])
    # tags: list[str]
    if 'tags' in meta:
        tags = meta['tags'].split(',')
        tags = [t.strip() for t in tags]
        meta['tags'] = tags

    return content, meta


class MarkdownLinkTreeprocessor(Treeprocessor):
    """Converts relative links to .md files to .html

    """

    def run(self, root):
        for element in root.iter():
            if element.tag == 'a':
                url = element.get('href')
                converted = self.convert(url)
                element.set('href', converted)
        return root

    def convert(self, url):
        scheme, netloc, path, query, fragment = urlsplit(url)
        logger.debug(f'{url} -> scheme: {scheme} netloc: {netloc} path: {path} query: {query} fragment: {fragment}')
        if (scheme or netloc or not path):
            return url
        if path.endswith('.md'):
            path = path[:-3] + '.html'

        url = urlunsplit((scheme, netloc, path, query, fragment))
        return url


class MarkdownLinkExtension(Extension):
    def extendMarkdown(self, md):
        md.treeprocessors.register(
                MarkdownLinkTreeprocessor(md), 'mdlink', 0,
        )


if __name__ == '__main__':
    main()
