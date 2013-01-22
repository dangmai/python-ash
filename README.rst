==========
python-ash
==========

Ash is a thin wrapper around the excellent `virtualenv`_ that parallels the
behavior by `npm`_. This generally means that the virtual environment for a
project is directly inside the project directory structure. This is different to
the approach by `virtualenvwrapper`_ - that is, a centralized place for
virtualenvs. By coupling the environment to the project itself, developers don't
have to remember to switch among different environments when they work on
different projects.

Ash tries to be as cross platform as possible. As of this moment, I've used Ash
successfully on Windows and Linux. If you can help with testing/debugging Ash on
other platforms, I would appreciate it very much.

Installation
============

Put ``ash.py`` into a directory in your PATH. That's it.

Or you could go the easy route and use `pip`_ like the following::

    pip install ash

to install Ash on your system.

Usage
=====

It is very easy to use ash, in fact, it tries to stay out of the way as much as
possible. The only special command for Ash is::

    ash.py init

which initializes the virtualenv for the current directory. All the options for
virtualenv are allowed here, for example::

    ash.py init --distribute --relocatable

The init command will create a ``python_env`` directory (the directory name is
modifiable via the `Configuration`_) in the current directory which contains
your brand new virtualenv. Afterwards, you can run any command with the
following syntax in this directory (and/or its subdirectories)::

    ash.py *your command here*

and it will be run in the created virtual environment. For example::

    ash.py pip install Django

will install Django into your ``python_env`` directory. That is all there is to
it.

*Note*: It is recommended that you include the ``python_env`` directory in your
ignore file for version control softwares, so that the environment itself is not
checked in.

Configuration
=============

Ash allows you to specify configurations for its behavior by adding a file named
``.ashconfig`` in your ``HOME`` folder (in Linux, this is ``~/.ashconfig``, in
Windows, it is usually ``C:\Users\yourusername\.ashconfig``). This config file
is in JSON format, and at the moment the following settings (with their default
values) are available::

    {
        "debug": false,  # set to true for more verbose debugs
        "venv_command": "virtualenv",  # for irregular path to virtualenv
        "venv_dir_name": "python_env"  # the name to use for the env directory
    }

.. _virtualenv: http://www.virtualenv.org
.. _npm: https://npmjs.org/
.. _virtualenvwrapper: http://www.doughellmann.com/projects/virtualenvwrapper/
.. _pip: http://www.pip-installer.org