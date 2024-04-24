"""Helper methods for blag's quickstart command."""

import argparse
import configparser
import os
import shutil

import blag


def get_input(question: str, default: str) -> str:
    """Prompt for user input.

    This is a wrapper around the input-builtin. It will show the default answer
    in the prompt and -- if no answer was given -- use the default.

    Parameters
    ----------
    question
        the question the user is presented
    default
        the default value that will be used if no answer was given

    Returns
    -------
    str
        the answer

    """
    reply = input(f"{question} [{default}]: ")
    if not reply:
        reply = default
    return reply


def copy_default_theme() -> None:
    """Copy default theme into current directory.

    The default theme contains the 'templates', 'content' and 'static'
    directories shipped with blag.

    It will not overwrite existing files.

    """
    print("Copying default theme...")
    for dir_ in "templates", "content", "static":
        print(f"  Copying {dir_}...")
        try:
            shutil.copytree(
                os.path.join(blag.__path__[0], dir_),
                dir_,
            )
        except FileExistsError:
            print(f"  {dir_} already exist. Skipping.")


def quickstart(args: argparse.Namespace | None) -> None:
    """Quickstart.

    This method asks the user some questions and generates a configuration file
    that is needed in order to run blag. Additionally, it creates the content
    and static directories with some initial content, to get the user started.

    Parameters
    ----------
    args
        not used

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
    config["main"] = {
        "base_url": base_url,
        "title": title,
        "description": description,
        "author": author,
    }
    with open("config.ini", "w") as fh:
        config.write(fh)

    copy_default_theme()
