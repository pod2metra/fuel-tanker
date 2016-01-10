# coding: utf-8
import os
import cStringIO
import subprocess
import tempfile
import tarfile


def archive_dirs(archive, src_path, tag_name):
    """Archive all dirs from src path to archive
       with name like {tag_name}/{dir_name} """
    if not os.path.exists(src_path):
        return
    for directory in os.listdir(src_path):
        dirpath = os.path.join(src_path, directory)
        if not os.path.isdir(dirpath):
            continue
        if os.path.islink(dirpath):
            continue
        archive.add(dirpath, "{0}/{1}".format(tag_name, directory))


def extract_tag_to(archive, tag, dst_dir):
    """Extract all members from archive with current tag to destination dir"""
    for member in archive:
        if not (member.name.startswith(tag) and member.isfile()):
            continue
        member.name = member.name.split("/", 1)[1]
        archive.extract(member, dst_dir)


def exec_cmd_in_container(container, cmd):
    process = subprocess.Popen(
        ["dockerctl", "shell", container] + cmd.strip().split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    data, _ = process.communicate()
    process.wait()
    return data


def archivate_container_cmd_output(
        archive, container, command, archive_path):
    info = tarfile.TarInfo(archive_path)
    dump = cStringIO.StringIO()
    data = exec_cmd_in_container(container, command)
    info.size = len(data)
    dump.write(data)
    dump.seek(0)
    archive.addfile(info, dump)


def restore_file_in_container(archive, container, tag, container_path):
    """restore file by tag name from archive in current
       container path in container"""

    proc = subprocess.Popen([
        "docker",
        "ps",
        "--filter",
        "name={0}".format(container),
        '--format="{{.Names}}"'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    name, _ = proc.communicate()
    name = name.strip()
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(archive.extractfile(tag).read())
    temp.close()
    subprocess.call([
        "docker", "cp", temp.name, "{0}:{1}".format(name, container_path)
    ])
    os.remove(temp.name)
