# -*- coding: utf-8 -*-
# taken from https://github.com/pypa/virtualenv and modified
"""Activate virtualenv for current interpreter:
Use exec(open(this_file).read(), {'__file__': this_file}).
This can be used when you must use an existing Python interpreter, not the virtualenv bin/python.
"""
import os
import site
import sys

try:
    abs_file = os.path.abspath(__file__)
except NameError:
    raise AssertionError("You must use exec(open(this_file).read(), {'__file__': this_file}))")

bin_dir = os.path.dirname(abs_file)
base = bin_dir[: -len("bin") - 1]  # strip away the bin part from the __file__, plus the path separator
base_dir = bin_dir[: -len("bin") ]  # strip away the bin part from the __file__, 

# prepend bin to PATH (this file is inside the bin directory)
os.environ["PATH"] = os.pathsep.join([bin_dir] + os.environ.get("PATH", "").split(os.pathsep))
os.environ["VIRTUAL_ENV"] = base  # virtual env is right above bin directory

# add the virtual environments libraries to the host python import mechanism
prev_length = len(sys.path)
for lib in "lib/python3.8/site-packages/".split(os.pathsep):
    path = os.path.realpath(os.path.join(base_dir, lib))
    print(path)
    print(lib)
    site.addsitedir(path)
sys.path[:] = sys.path[prev_length:] + sys.path[0:prev_length]

sys.real_prefix = sys.prefix
sys.prefix = base
