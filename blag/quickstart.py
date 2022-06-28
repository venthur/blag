"""Helper methods for blag's quickstart command.

"""

import configparser


def get_input(question, default):
    """Prompt for user input.

    This is a wrapper around the input-builtin. It will show the default answer
    in the prompt and -- if no answer was given -- use the default.

    Parameters
    ----------
    question : str
        the question the user is presented
    default : str
        the default value that will be used if no answer was given

    Returns
    -------
    str

    """
    reply = input(f"{question} [{default}]: ")
    if not reply:
        reply = default
    return reply


def quickstart(args):
    """Quickstart.

    This method asks the user some questions and generates a
    configuration file that is needed in order to run blag.

    Parameters
    ----------
    args : argparse.Namespace

    """
    base_url = get_input(
        "Hostname (and path) to the root?",
        "https://example.com/",
    )
    title = get_input(
        "Title of your website?",
        "My little blog",
    )
    description = get_input(
        "Description of your website?",
        "John Doe's Blog",
    )
    author = get_input(
        "Author of your website",
        "John Doe",
    )

    config = configparser.ConfigParser()
    config['main'] = {
            'base_url': base_url,
            'title': title,
            'description': description,
            'author': author,
    }
    with open('config.ini', 'w') as fh:
        config.write(fh)
