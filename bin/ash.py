#!/usr/bin/env python

import os
import sys
import subprocess
import logging
import json

logger = logging.getLogger("ash")


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


def _get_env_dir(venv_dir_name):
    """
    Get the virtualenv from this dir or parent dirs. If no virtualenv is found,
    this returns False
    """
    for curr_dir, included_dirs, included_files in _walk_up(os.getcwd()):
        if venv_dir_name in included_dirs:
            env = os.path.join(curr_dir, venv_dir_name)
            logger.debug("virtualenv found! %s", env)
            return env
    logger.debug("No virtualenv found with dir name %s" % (venv_dir_name))
    return False


def _check_virtualenv(venv_command):
    """
    Check for the existence of virtualenv
    """
    try:
        command = "%s --version" % (venv_command)
        logger.debug("Checking virtualenv with command: %s" % (command))
        subprocess.call(command, stdout=open(os.devnull, 'wb'))
    except:
        return False
    return True


def _create_venv(venv_command, directory, args):
    """
    Create a virtual environment. Right now it is using virtualenv through the
    command line, but later on I may change this to the virtualenv API, or venv
    in later versions of Python 3.
    """
    if args:
        command = "%s %s %s" % (venv_command, args, directory)
    else:
        command = "%s %s" % (venv_command, directory)
    logger.debug("Create env with command: %s", command)
    return subprocess.call(command)


def _activate_venv(dir):
    """
    Activate a virtualenv, given its directory.
    """
    activate_file = os.path.join(dir, "Scripts", "activate_this.py")
    logger.debug("Activating virtualenv with file %s", activate_file)
    execfile(activate_file, dict(__file__=activate_file))


def _get_config():
    """
    Get the config for this program, returning a dict with the settings.
    """
    default_config = {
        "venv_command": "virtualenv",
        "venv_dir_name": "python_env",
        "debug": False
    }
    config = {}  # the config that is read from the config file
    config_location = os.path.join(os.path.expanduser("~"), ".ashconfig")
    if (os.path.exists(config_location)):
        config_file = open(config_location, "r")
        config = json.loads(config_file.read())
        config_file.close()
    result = default_config.copy()
    result.update(config)
    return result


def main():
    config = _get_config()
    # Configure logging
    logger.setLevel(logging.DEBUG)  # baseline level, fine tune later on
    log_handler = logging.StreamHandler()
    if not config["debug"]:
        log_handler.setLevel(logging.INFO)
        log_handler.setFormatter(logging.Formatter('%(message)s'))
    else:
        log_handler.setLevel(logging.DEBUG)
        log_handler.setFormatter(
            logging.Formatter(
                '%(levelname)s %(asctime)s: %(message)s'
            )
        )
    logger.addHandler(log_handler)
    logger.debug("Program configured and ready to roll")

    if not _check_virtualenv(config["venv_command"]):
        logger.warning("It seems that virtualenv is not installed on this " +
            "system. Exiting now.")
        sys.exit(3)

    if len(sys.argv) <= 1:
        logger.info("Do something!")
        sys.exit(2)
    venv = _get_env_dir(config["venv_dir_name"])

    if sys.argv[1] == "init":
        if venv:
            logger.warning("You are already inside a virtual environment!")
            sys.exit(1)
        args = " ".join(sys.argv[2:]) if (len(sys.argv) > 2) else None

        sys.exit(_create_venv(config["venv_command"],
            os.path.join(os.getcwd(), config["venv_dir_name"]), args))

    _activate_venv(venv)
    command = " ".join(sys.argv[1:])
    logger.debug("Command to call: %s", command)
    subprocess.call(command, shell=True)

if __name__ == "__main__":
    main()
