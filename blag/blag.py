#!/usr/bin/env python3

"""Small static site generator.

"""


__author__ = "Bastian Venthur <venthur@debian.org>"


import argparse
import os
import shutil
import logging

from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader
import feedgenerator

from blag.markdown import markdown_factory, convert_markdown

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
    build_parser.add_argument(
            '-t', '--template-dir',
            default='templates',
            help='Template directory (default: templates)',
    )
    return parser.parse_args()


def build(args):
    os.makedirs(f'{args.output_dir}', exist_ok=True)
    convertibles = []
    for root, dirnames, filenames in os.walk(args.input_dir):
        for filename in filenames:
            rel_src = os.path.relpath(f'{root}/{filename}',
                                      start=args.input_dir)
            # all non-markdown files are just copied over, the markdown
            # files are converted to html
            if rel_src.endswith('.md'):
                rel_dst = rel_src
                rel_dst = rel_dst[:-3] + '.html'
                convertibles.append((rel_src, rel_dst))
            else:
                shutil.copy(f'{args.input_dir}/{rel_src}',
                            f'{args.output_dir}/{rel_src}')
        for dirname in dirnames:
            # all directories are copied into the output directory
            path = os.path.relpath(f'{root}/{dirname}', start=args.input_dir)
            os.makedirs(f'{args.output_dir}/{path}', exist_ok=True)

    process_markdown(
        convertibles, args.input_dir,
        args.output_dir,
        args.template_dir
    )


def process_markdown(convertibles, input_dir, output_dir, template_dir):
    """Process markdown files.

    This method processes the convertibles, converts them to html and
    saves them to the respective destination paths.

    If a markdown file has a `date` metadata field it will be recognized
    as article otherwise as page.

    Parameters
    ----------
    convertibles : List[Tuple[str, str]]
        relative paths to markdown- (src) html- (dest) files
    input_dir : str
    output_dir : str
    template_dir : str

    Returns
    -------
    articles, pages : List[Tuple[str, Dict]]

    """
    env = Environment(
            loader=ChoiceLoader([
                FileSystemLoader([template_dir]),
                PackageLoader('blag', 'templates'),
            ])
    )

    md = markdown_factory()

    articles = []
    pages = []
    for src, dst in convertibles:
        logger.debug(f'Processing {src}')
        with open(f'{input_dir}/{src}', 'r') as fh:
            body = fh.read()

        content, meta = convert_markdown(md, body)

        context = dict(content=content)
        context.update(meta)

        # if markdown has date in meta, we treat it as a blog article,
        # everything else are just pages
        if meta and 'date' in meta:
            articles.append((dst, context))
            template = env.get_template('article.html')
        else:
            pages.append((dst, content))
            template = env.get_template('page.html')
        result = template.render(context)
        with open(f'{output_dir}/{dst}', 'w') as fh_dest:
            fh_dest.write(result)

    # sort articles by date, descending
    articles = sorted(articles, key=lambda x: x[1]['date'], reverse=True)

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
    archive = []
    for dst, context in articles:
        entry = context.copy()
        entry['dst'] = dst
        archive.append(entry)

    template = env.get_template('archive.html')
    result = template.render(dict(archive=archive))
    with open('build/index.html', 'w') as fh:
        fh.write(result)

    return articles, pages


if __name__ == '__main__':
    main()
