#!/usr/bin/env python

from distutils.core import setup

setup(name='multiscaleDlSurrogate',
      version='1.0',
      description='python codes codes to create Tensorflow based suorrogate model for lammps simulation data and deploy in FeniCS',
      author='Md Shahrier Hasan',
      author_email='rahat084@gmail.com',
      url='https://github.com/Rahat084',
      packages=['curation', 'training', 'deployment'],
     )
