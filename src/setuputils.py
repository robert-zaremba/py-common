import platform
from subprocess import call
import sys

import setuptools.command.build_py
from setuptools.command.test import test as TestCommand


class PyTestCommand(TestCommand):
    '''Enhanced test command to support awesome py.test'''

    user_options = [
            ('exitfirst', 'x', "exit on first error or failed test."),
            ('last-failed', 'l',
             "rerun only the tests that failed at the last run"),
            ('verbose', 'v', "increase verbosity"),
            ('pdb', 'p', "run pdb upon failure"),
            ('flakes', 'f', "run flakes on .py files"),
            ('pytest-args=', 'a', "Extra arguments to pass into py.test"),
            ]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = set()
        self.exitfirst = False
        self.last_failed = False
        self.verbose = 0
        self.pdb = False
        self.flakes = False

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        if isinstance(self.pytest_args, str):
            self.pytest_args = set(self.pytest_args.split(' '))
        if self.exitfirst:   self.pytest_args.add('-x')
        if self.pdb:         self.pytest_args.add('--pdb')
        if self.last_failed: self.pytest_args.add('--last-failed')
        if self.flakes:      self.pytest_args.add('--flakes')
        self.pytest_args = list(self.pytest_args)
        if self.verbose:
            for v in range(self.verbose):
                self.pytest_args.append('-v')
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class BuildPyCommand(setuptools.command.build_py.build_py):
    '''Enhanced build command to automatically build manpages'''

    def run(self):
        if platform.system() != 'Windows':
            self.run_command('build_manpage')
        setuptools.command.build_py.build_py.run(self)


class BuildDocsCommand(setuptools.command.build_py.build_py):
    apidoc_command = (
        'sphinx-apidoc', '-f', '-o', 'docs', '--no-toc', 'coalib'
    )
    doc_command = ('make', '-C', 'docs', 'html', 'SPHINXOPTS=-W')

    def run(self):
        errOne = call(self.apidoc_command)
        errTwo = call(self.doc_command)
        sys.exit(errOne or errTwo)


def read_requirements(*filenames):
    out = []
    for fn in filenames:
        out.append(_get_requirements(fn))
    return out


def _get_requirements(requirements_file):
    """Get the contents of a file listing the requirements"""
    with open(requirements_file) as f:
        lines = f.readlines()
    dependencies = []
    for l in lines:
        dep = l.strip()
        if dep.startswith('#'):  # Skip pure comment lines
            continue
        if dep.startswith('git+'):
            # VCS reference for dev purposes, expect a trailing comment
            # with the normal requirement
            __, __, dep = dep.rpartition('#')
        else:
            # Ignore any trailing comment
            dep, __, __ = dep.partition('#')
        # Remove any whitespace and assume non-empty results are dependencies
        dep = dep.strip()
        if dep:
            dependencies.append(dep)
    return dependencies
