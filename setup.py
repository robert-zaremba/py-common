#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Robert Zaremba
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from setuptools import setup, Command  # , find_packages
from glob import glob
import os
from os.path import splitext, basename, join as pjoin

try:
    import nose
except ImportError:
    nose = None
try:
    import pytest
except ImportError:
    pytest = None


class TestCommand(Command):
    """Custom distutils command to run the test suite."""

    user_options = []

    def initialize_options(self):
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run_nose(self):
        """Run the test suite with nose."""
        return nose.core.TestProgram(argv=["", '-vv',
                                           pjoin(self._dir, 'tests')])

    def run_unittest(self):
        """Finds all the tests modules in zmq/tests/ and runs them."""
        from unittest import TextTestRunner, TestLoader

        testfiles = []
        for t in glob(pjoin(self._dir, 'tests', '*.py')):
            name = splitext(basename(t))[0]
            if name.startswith('test_'):
                testfiles.append('.'.join(
                    ['tests', name])
                )
        tests = TestLoader().loadTestsFromNames(testfiles)
        t = TextTestRunner(verbosity=2)
        t.run(tests)

    def run_pytest(self):
        import subprocess
        errno = subprocess.call(['py.test', '-q'])
        raise SystemExit(errno)

    def run(self):
        """Run the test suite, with py.test, nose, or unittest
        (first which is available)"""
        if pytest:
            self.run_pytest()
        elif nose:
            print("# pytest unavailable, trying test with nose. Some tests \
might not run, and some skipped, xfailed will appear as ERRORs.")
            self.run_nose()
        else:
            print("# pytest and nose unavailable, falling back on unittest. \
Skipped tests will appear as ERRORs.")
            return self.run_unittest()


setup(
    name='pycommon',
    version='0.5',
    use_2to3=True,
    cmdclass={'test': TestCommand},
    description="Common modules which you may need for your daily projects",
    author='Robert Zaremba',
    author_email='robert.zaremba@scale-it.pl',
    url='https://github.com/robert-zaremba/py-common',
    download_url="https://github.com/robert-zaremba/py-common/tarball/master",
    license='Apache License',
    keywords="python common library utilities utils",
    package_dir={'pycommon': 'src'},
    packages=['pycommon'],
    zip_safe=True,
    test_suite="nose.collector",
    # tests_require=['py.test'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache License',
        "Programming Language :: Python",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: PyPy',
        'Operating System :: OS Independent',
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
    ],
)
