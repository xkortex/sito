from pkg_resources import get_distribution, DistributionNotFound

__version__ = "0+unknown"

try:
    __version__ = get_distribution(__name__).version
    print("pkg_resources")
except (DistributionNotFound, NameError) as exc:
    # package is not installed
    from sito import __version__
