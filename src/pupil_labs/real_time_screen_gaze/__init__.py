"""Top-level entry-point for the real_time_screen_gaze package"""

try:
    from importlib.metadata import PackageNotFoundError, version
except ImportError:
    from importlib_metadata import PackageNotFoundError, version

try:
    __version__ = version("pupil_labs.real_time_screen_gaze")
except PackageNotFoundError:
    # package is not installed
    pass

__all__ = ["__version__"]
