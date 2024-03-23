#!/usr/bin/python3
"""Fabric script that generates a .tgz
archive from the contents of the web_static folder
of your AirBnB Clone repo, using the function do_pack."""

from fabric.api import local
from datetime import datetime


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
