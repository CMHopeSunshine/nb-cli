#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__version__ = "0.1.0"

import sys
import click

from nb_cli.utils import ClickAliasedGroup
from nb_cli.handlers import run_bot, create_project, _call_docker_compose, handle_no_subcommand

sys.path.insert(0, ".")


@click.group(cls=ClickAliasedGroup, invoke_without_command=True)
@click.version_option(__version__,
                      "-V",
                      "--version",
                      message="%(prog)s: nonebot cli version %(version)s")
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        handle_no_subcommand()


@main.command(aliases=["create"])
def init():
    """Create A NoneBot Project"""
    create_project()


@main.command(aliases=["start"])
@click.option("-f",
              "--file",
              default="bot.py",
              show_default=True,
              help="Entry file of your bot")
@click.option("-a",
              "--app",
              default="app",
              show_default=True,
              help="ASGI application of your bot")
def run(file, app):
    """Run the Bot in Current Folder"""
    run_bot(file, app)


@main.command(context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def build(args):
    """Build Docker Image for Bot in Current Folder.
    The same as docker-compose build.
    
    Options see: https://docs.docker.com/compose/reference/build/
    """
    _call_docker_compose("build", args)


@main.command(aliases=["up"], context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def deploy(args):
    """Builds, (Re)Creates, Starts Containers for Bot in Current Folder.
    The same as docker-compose up -d.
    
    Options see: https://docs.docker.com/compose/reference/up/
    """
    if "-d" not in args:
        args = ["-d", *args]
    _call_docker_compose("up", args)


@main.command(aliases=["down"],
              context_settings={"ignore_unknown_options": True})
@click.argument("args", nargs=-1, type=click.UNPROCESSED)
def exit(args):
    """Stops Containers and Removes Containers, Networks, Volumes and Images for Bot in Current Folder.
    The same as docker-compose down.
    
    Options see: https://docs.docker.com/compose/reference/down/"""
    _call_docker_compose("down", args)


if __name__ == "__main__":
    main()
