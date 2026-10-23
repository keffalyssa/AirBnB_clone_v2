#!/usr/bin/python3
"""Fabric script that creates and distributes an archive to web servers.

Usage:
    fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
"""
from datetime import datetime
from fabric.api import env, local, put, run, runs_once
from os.path import exists, isdir

env.hosts = ['<IP web-01>', '<IP web-02>']


@runs_once
def do_pack():
    """Generate a .tgz archive from the web_static folder."""
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if not isdir("versions"):
            local("mkdir -p versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local("tar -cvzf {} web_static".format(file_name))
        return file_name
    except Exception:
        return None


def do_deploy(archive_path):
    """Distribute an archive to the web servers."""
    if not exists(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        path = "/data/web_static/releases/"
        put(archive_path, "/tmp/{}".format(file_name))
        run("mkdir -p {}{}/".format(path, no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(file_name, path, no_ext))
        run("rm /tmp/{}".format(file_name))
        run("mv {0}{1}/web_static/* {0}{1}/".format(path, no_ext))
        run("rm -rf {}{}/web_static".format(path, no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False


def deploy():
    """Create and distribute an archive to the web servers."""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
