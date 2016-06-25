import pytest

def pytest_addoption(parser):
    parser.addoption('--runslow', action='store_true', help='runs slow tests')
