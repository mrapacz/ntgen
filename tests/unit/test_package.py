import pkg_resources

import ntgen


def test_consistent_package_version():
    """Tests that the package version in setup.py and ntgen.__init__ are the same."""
    assert pkg_resources.require("ntgen")[0].version == ntgen.__version__
