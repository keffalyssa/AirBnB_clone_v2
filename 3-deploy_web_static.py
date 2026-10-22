#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers."""
from fabric.api import env, local, put, run
from datetime import datetime
from os.path import exists, basename, splitext

env.hosts = ['<IP web-01>', '<IP web-02>']


def do_pack():
    """Generates a .tgz archive from the web_static folder."""
    try:
        now = datetime.now().strftime("%Y%m%d%H%M%S")
        path = "versions/web_static_{}.tgz".format(now)
        local("mkdir -p versions")
        local("tar -cvzf {} web_static".format(path))
        return path
    except Exception:
        return None


def do_deploy(archive_path):
    """Distributes an archive to the web servers.

    Returns True if all operations succeeded, otherwise False.
    """
    if not exists(archive_path):
        return False

    try:
        file_name = basename(archive_path)
        name = splitext(file_name)[0]
        release = "/data/web_static/releases/{}/".format(name)
        tmp_path = "/tmp/{}".format(file_name)

        put(archive_path, tmp_path)
        run("mkdir -p {}".format(release))
        run("tar -xzf {} -C {}".format(tmp_path, release))
        run("rm {}".format(tmp_path))
        run("mv {0}web_static/* {0}".format(release))
        run("rm -rf {}web_static".format(release))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Creates and distributes an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
