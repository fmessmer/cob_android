#!/usr/bin/env python

from distutils.core import setup
from catkin_pkg.python_setup import generate_distutils_setup

d = generate_distutils_setup(
   packages=['cob_android_resource_server'],
   package_dir={'': 'src'},
   scripts['scripts/resource_server'],
   requires=['rospkg']
)

setup(**d)
