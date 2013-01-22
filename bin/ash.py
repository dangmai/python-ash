#!/usr/bin/env python

import os
import sys
import subprocess
import logging

ENV_DIR_NAME = "python_env"


def _walk_up(bottom):
    """
    walk up a dir tree. Code adapted from https://gist.github.com/1098474
    """
    bottom = os.path.realpath(bottom)
    #get files in current dir
    names = os.listdir(bottom)
    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)
    yield bottom, dirs, nondirs
    new_path = os.path.realpath(os.path.join(bottom, '..'))

    # see if we are at the top
    if new_path == bottom:
        return
    for x in _walk_up(new_path):
        yield x


def _get_env_dir():
    """
    Get the virtualenv from this dir or parent dirs. If no virtualenv is found,
    this returns False
    """
    for curr_dir, included_dirs, included_files in _walk_up(os.getcwd()):
        if ENV_DIR_NAME in included_dirs:
            env = os.path.join(curr_dir, ENV_DIR_NAME)
            logging.debug("virtualenv found! %s", env)
            return env
    logging.debug("No virtualenv found")
    return False


def _check_virtualenv():
    """
    Check for the existence of virtualenv
    """
    try:
        subprocess.call("virtualenv --version", stdout=open(os.devnull, 'wb'))
    except:
        return False
    return True


def _create_venv(directory, args):
    """
    Create a virtual environment. Right now it is using virtualenv through the
    command line, but later on I may change this to the virtualenv API, or venv
    in later versions of Python 3.
    """
    if args:
        command = "virtualenv %s %s" % (args, directory)
    else:
        command = "virtualenv %s" % (directory)
    logging.debug("Create env with command: %s", command)
    return subprocess.call(command)


def _activate_venv(dir):
    """
    Activate a virtualenv, given its directory.
    """
    activate_file = os.path.join(dir, "Scripts", "activate_this.py")
    logging.debug("Activating virtualenv with file %s", activate_file)
    execfile(activate_file, dict(__file__=activate_file))


def main():
    if "ASH_DEBUG" in os.environ and os.environ["ASH_DEBUG"] == "TRUE":
        # Allow for debugging
        logging.basicConfig(level=logging.DEBUG)
    logging.info("Main called")
    if not _check_virtualenv():
        print("It seems that virtualenv is not installed on this system. " +
            "Exiting now.")
        sys.exit(3)

    if len(sys.argv) <= 1:
        print("Do something!")
        sys.exit(2)
    venv = _get_env_dir()

    if sys.argv[1] == "init":
        if venv:
            print("You are already inside a virtual environment!")
            sys.exit(1)
        args = " ".join(sys.argv[2:]) if (len(sys.argv) > 2) else None

        sys.exit(_create_venv(os.path.join(os.getcwd(), ENV_DIR_NAME), args))

    _activate_venv(venv)
    command = " ".join(sys.argv[1:])
    logging.info("Command to call: %s", command)
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
