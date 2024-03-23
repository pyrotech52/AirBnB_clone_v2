#!/usr/bin/python3
"""Fabric script that generates a .tgz
archive from the contents of the web_static folder."""

from fabric.api import local, put, env, run
from datetime import datetime
from os.path import exists
env.hosts = ['54.242.35.218', '50.16.118.128']


def do_pack():
    """ The function do_pack """
    local("mkdir -p versions")
    time = datetime.strftime(datetime.now(), "%Y%m%d%H%M%S")
    file = "versions/web_static_{}.tgz".format(time)

    try:
        local("tar -czvf {} web_static".format(file))
        return file

    except Exception:
        return None


def do_deploy(archive_path):
    """ do_deploy """
    if not exists(archive_path):
        return False
    try:
        """archive_path = versions/web_static_20170315003959.tgz """
        file_name = archive_path.split("/")[-1]
        """file_name = web_static_20170315003959.tgz"""
        no_ext = file_name.split(".")[0]
        """no_ext = web_static_20170315003959"""
        path = "/data/web_static/releases/"
        """Upload the archive to the /tmp/ directory of the web server"""
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(path, no_ext))
        """Uncompress the archive"""
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, path, no_ext))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(path, no_ext))
        run('rm -rf {}{}/web_static'.format(path, no_ext))
        run('rm -rf /data/web_static/current')
        run('ln -s {}{}/ /data/web_static/current'.format(path, no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False


"""fab -f 2-do_deploy_web_static.py do_deploy:
archive_path=versions/web_static_20220824140539.tgz -i
/home/vagrant/.ssh/school -u ubuntu"""


def deploy():
    """deploy"""
    archive = do_pack()
    if archive is None:
        return False
    return do_deploy(archive)


"""fab -f 3-deploy_web_static.py deploy -i
/home/vagrant/.ssh/school -u ubuntu"""
