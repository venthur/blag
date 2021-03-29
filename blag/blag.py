#!/usr/bin/env python3

"""blag's core methods.

"""

import argparse
import os
import shutil
import logging
import configparser
import sys

from jinja2 import Environment, ChoiceLoader, FileSystemLoader, PackageLoader
import feedgenerator

from blag.markdown import markdown_factory, convert_markdown
from blag.devserver import serve

logger = logging.getLogger(__name__)
logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
)


def main(args=None):
    """Main entrypoint for the CLI.

    This method parses the CLI arguments and executes the respective
    commands.

    Parameters
    ----------
    args : list[str]
        optional parameters, used for testing

    """
    args = parse_args(args)
    args.func(args)


def parse_args(args=None):
    """Parse command line arguments.

    Parameters
    ----------
    args : List[str]
        optional parameters, used for testing

    Returns
    -------
    arparse.Namespace

    """
    parser = argparse.ArgumentParser()

    commands = parser.add_subparsers(dest='command')
    commands.required = True

    build_parser = commands.add_parser(
            'build',
            help='Build website.',
    )
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
    build_parser.add_argument(
            '-s', '--static-dir',
            default='static',
            help='Static directory (default: static)',
    )

    quickstart_parser = commands.add_parser(
            'quickstart',
            help="Quickstart blag, creating necessary configuration.",
    )
    quickstart_parser.set_defaults(func=quickstart)

    serve_parser = commands.add_parser(
            'serve',
            help="Start development server.",
    )
    serve_parser.set_defaults(func=serve)
    serve_parser.add_argument(
            '-i', '--input-dir',
            default='content',
            help='Input directory (default: content)',
    )
    serve_parser.add_argument(
            '-o', '--output-dir',
            default='build',
            help='Ouptut directory (default: build)',
    )
    serve_parser.add_argument(
            '-t', '--template-dir',
            default='templates',
            help='Template directory (default: templates)',
    )
    serve_parser.add_argument(
            '-s', '--static-dir',
            default='static',
            help='Static directory (default: static)',
    )

    return parser.parse_args(args)


def get_config(configfile):
    """Load site configuration from configfile.

    Parameters
    ----------
    configfile : str
        path to configuration file


    Returns
    -------
    dict

    """
    config = configparser.ConfigParser()
    config.read(configfile)
    # check for the mandatory options
    for value in 'base_url', 'title', 'description', 'author':
        try:
            config['main'][value]
        except Exception:
            print(f'{value} is missing in {configfile}!')
            sys.exit(1)

    if not config['main']['base_url'].endswith('/'):
        logger.warning('base_url does not end with a slash, adding it.')
        config['main']['base_url'] += '/'

    return config['main']


def environment_factory(template_dir=None, globals_=None):
    """Environment factory.

    Creates a Jinja2 Environment with the default templates and
    additional templates from `template_dir` loaded. If `globals` are
    provided, they are attached to the environment and thus available to
    all contexts.

    Parameters
    ----------
    template_dir : str
    globals_ : dict

    Returns
    -------
    jinja2.Environment

    """
    # first we try the custom templates, and fall back the ones provided
    # by blag
    loaders = []
    if template_dir:
        loaders.append(FileSystemLoader([template_dir]))
    loaders.append(PackageLoader('blag', 'templates'))
    env = Environment(loader=ChoiceLoader(loaders))
    if globals_:
        env.globals = globals_
    return env


def build(args):
    """Build the site.

    This is blag's main method that builds the site, generates the feed
    etc.

    Parameters
    ----------
    args : argparse.Namespace

    """
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

    # copy static files over
    if os.path.exists(args.static_dir):
        shutil.copytree(args.static_dir, args.output_dir, dirs_exist_ok=True)

    config = get_config('config.ini')

    env = environment_factory(args.template_dir, dict(site=config))

    page_template = env.get_template('page.html')
    article_template = env.get_template('article.html')
    archive_template = env.get_template('archive.html')
    tags_template = env.get_template('tags.html')
    tag_template = env.get_template('tag.html')

    articles, pages = process_markdown(
        convertibles,
        args.input_dir,
        args.output_dir,
        page_template,
        article_template,
    )

    generate_feed(
        articles, args.output_dir,
        base_url=config['base_url'],
        blog_title=config['title'],
        blog_description=config['description'],
        blog_author=config['author'],
    )
    generate_archive(articles, archive_template, args.output_dir)
    generate_tags(articles, tags_template, tag_template, args.output_dir)


def process_markdown(convertibles, input_dir, output_dir,
                     page_template, article_template):
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
    page_template, archive_template : jinja2 template
        templats for pages and articles

    Returns
    -------
    articles, pages : List[Tuple[str, Dict]]

    """
    logger.info("Converting Markdown files...")
    md = markdown_factory()

    articles = []
    pages = []
    for src, dst in convertibles:
        logger.info(f'Processing {src}')
        with open(f'{input_dir}/{src}', 'r') as fh:
            body = fh.read()

        content, meta = convert_markdown(md, body)

        context = dict(content=content)
        context.update(meta)

        # if markdown has date in meta, we treat it as a blog article,
        # everything else are just pages
        if meta and 'date' in meta:
            articles.append((dst, context))
            result = article_template.render(context)
        else:
            pages.append((dst, context))
            result = page_template.render(context)
        with open(f'{output_dir}/{dst}', 'w') as fh_dest:
            fh_dest.write(result)

    # sort articles by date, descending
    articles = sorted(articles, key=lambda x: x[1]['date'], reverse=True)
    return articles, pages


def generate_feed(
        articles,
        output_dir,
        base_url,
        blog_title,
        blog_description,
        blog_author,
):
    """Generate Atom feed.

    Parameters
    ----------
    articles : list[list[str, dict]]
        list of relative output path and article dictionary
    output_dir : str
        where the feed is stored
    base_url : str
        base url
    blog_title : str
        blog title
    blog_description : str
        blog description
    blog_author : str
        blog author

    """
    logger.info('Generating Atom feed.')
    feed = feedgenerator.Atom1Feed(
            link=base_url,
            title=blog_title,
            description=blog_description,
            feed_url=base_url + 'atom.xml',
    )

    for dst, context in articles:
        # if article has a description, use that. otherwise fall back to
        # the title
        description = context.get('description', context['title'])

        feed.add_item(
            title=context['title'],
            author_name=blog_author,
            link=base_url + dst,
            description=description,
            content=context['content'],
            pubdate=context['date'],
        )

    with open(f'{output_dir}/atom.xml', 'w') as fh:
        feed.write(fh, encoding='utf8')


def generate_archive(articles, template, output_dir):
    """Generate the archive page.

    Parameters
    ----------
    articles : list[list[str, dict]]
        List of articles. Each article has the destination path and a
        dictionary with the content.
    template : jinja2.Template instance
    output_dir : str

    """
    archive = []
    for dst, context in articles:
        entry = context.copy()
        entry['dst'] = dst
        archive.append(entry)

    result = template.render(dict(archive=archive))
    with open(f'{output_dir}/index.html', 'w') as fh:
        fh.write(result)


def generate_tags(articles, tags_template, tag_template, output_dir):
    """Generate the tags page.

    Parameters
    ----------
    articles : list[list[str, dict]]
        List of articles. Each article has the destination path and a
        dictionary with the content.
    tags_template, tag_template : jinja2.Template instance
    output_dir : str

    """
    logger.info("Generating Tag-pages.")
    os.makedirs(f'{output_dir}/tags', exist_ok=True)

    # get tags number of occurrences
    all_tags = {}
    for _, context in articles:
        tags = context.get('tags', [])
        for tag in tags:
            all_tags[tag] = all_tags.get(tag, 0) + 1
    # sort by occurrence
    all_tags = sorted(all_tags.items(), key=lambda x: x[1], reverse=True)

    result = tags_template.render(dict(tags=all_tags))
    with open(f'{output_dir}/tags/index.html', 'w') as fh:
        fh.write(result)

    # get tags and archive per tag
    all_tags = {}
    for dst, context in articles:
        tags = context.get('tags', [])
        for tag in tags:
            archive = all_tags.get(tag, [])
            entry = context.copy()
            entry['dst'] = dst
            archive.append(entry)
            all_tags[tag] = archive

    for tag, archive in all_tags.items():
        result = tag_template.render(dict(archive=archive, tag=tag))
        with open(f'{output_dir}/tags/{tag}.html', 'w') as fh:
            fh.write(result)


def quickstart(args):
    """Quickstart.

    This method asks the user some questions and generates a
    configuration file that is needed in order to run blag.

    Parameters
    ----------
    args : argparse.Namespace

    """
    base_url = input("Hostname (and path) to the root? "
                     "[https://example.com/]: ")
    title = input("Title of your website? ")
    description = input("Description of your website [John Does's Blog]? ")
    author = input("Author of your website [John Doe]? ")

    config = configparser.ConfigParser()
    config['main'] = {
            'base_url': base_url,
            'title': title,
            'description': description,
            'author': author,
    }
    with open('config.ini', 'w') as fh:
        config.write(fh)


if __name__ == '__main__':
    main()
