import pytest


@pytest.fixture
def benchmark():
    """Simple stub for pytest-benchmark when plugin is not installed.

    This executes the provided callable and returns its result. It allows
    tests that rely on the 'benchmark' fixture to run without the plugin.
    """
    def _bench(func):
        return func()

    return _bench
