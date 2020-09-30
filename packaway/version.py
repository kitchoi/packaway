
_MAJOR = 0
_MINOR = 1
_MICRO = 1

#: One of 'alpha', 'beta', 'candidate', 'final'
_RELEASE_LEVEL = "final"

_SERIAL = 0

__version__ = "{}.{}.{}".format(_MAJOR, _MINOR, _MICRO)
__version__ += {
    "alpha": "a" + str(_SERIAL),
    "beta": "b" + str(_SERIAL),
    "candidate": "rc" + str(_SERIAL),
    "final": "",
}[_RELEASE_LEVEL]

__version_info__ = (
    _MAJOR, _MINOR, _MICRO, _RELEASE_LEVEL, _SERIAL
)
