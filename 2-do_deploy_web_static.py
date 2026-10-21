#!/usr/bin/python3
"""Fabric script that distributes an archive to web servers."""
from fabric.api import env, put, run, settings
import os

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_deploy(archive_path):
    """Deploy an archive to the web servers.

    Returns True if all operations succeeded, otherwise False.
    """
    if not os.path.isfile(archive_path):
        return False

    filename = os.path.basename(archive_path)
    name = filename.split(".")[0]
    release = "/data/web_static/releases/{}".format(name)
    tmp = "/tmp/{}".format(filename)

    with settings(warn_only=True):
        if put(archive_path, tmp).failed:
            return False
        commands = [
            "mkdir -p {}/".format(release),
            "tar -xzf {} -C {}/".format(tmp, release),
            "rm {}".format(tmp),
            "mv {}/web_static/* {}/".format(release, release),
            "rm -rf {}/web_static".format(release),
            "rm -rf /data/web_static/current",
            "ln -s {}/ /data/web_static/current".format(release),
        ]
        for cmd in commands:
            if run(cmd).failed:
                return False

    print("New version deployed!")
    return True
