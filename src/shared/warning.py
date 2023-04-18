import warnings

from requests import RequestsDependencyWarning  # type: ignore
from setuptools import SetuptoolsDeprecationWarning


def ignore_warnings():
    warnings.simplefilter("ignore", category=RequestsDependencyWarning)
    warnings.simplefilter("ignore", category=SetuptoolsDeprecationWarning)
