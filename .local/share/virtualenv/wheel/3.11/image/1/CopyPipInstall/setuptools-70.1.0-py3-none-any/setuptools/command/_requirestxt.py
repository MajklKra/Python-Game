"""Helper code used to generate ``requires.txt`` files in the egg-info directory.

The ``requires.txt`` file has an specific format:
    - Environment markers need to be part of the section headers and
      should not be part of the requirement spec itself.

See https://setuptools.pypa.io/en/latest/deprecated/python_eggs.html#requires-txt
"""

from __future__ import annotations

import io
from collections import defaultdict
from itertools import filterfalse
from typing import Dict, Mapping, TypeVar

from .. import _reqs
from ..extern.jaraco.text import yield_lines
from ..extern.packaging.requirements import Requirement


# dict can work as an ordered set
_T = TypeVar("_T")
_Ordered = Dict[_T, None]
_ordered = dict
_StrOrIter = _reqs._StrOrIter


def _prepare(
    install_requires: _StrOrIter, extras_require: Mapping[str, _StrOrIter]
) -> tuple[list[str], dict[str, list[str]]]:
    """Given values for ``install_requires`` and ``extras_require``
    create modified versions in a way that can be written in ``requires.txt``
    """
    extras = _convert_extras_requirements(extras_require)
    return _move_install_requirements_markers(install_requires, extras)


def _convert_extras_requirements(
    extras_require: Mapping[str, _StrOrIter],
) -> Mapping[str, _Ordered[Requirement]]:
    """
    Convert requirements in `extras_require` of the form
    `"extra": ["barbazquux; {marker}"]` to
    `"extra:{marker}": ["barbazquux"]`.
    """
    output: Mapping[str, _Ordered[Requirement]] = defaultdict(dict)
    for section, v in extras_require.items():
        # Do not strip empty sections.
        output[section]
        for r in _reqs.parse(v):
            output[section + _suffix_for(r)].setdefault(r)

    return output


def _move_install_requirements_markers(
    install_requires: _StrOrIter, extras_require: Mapping[str, _Ordered[Requirement]]
) -> tuple[list[str], dict[str, list[str]]]:
    """
    The ``requires.txt`` file has an specific format:
        - Environment markers need to be part of the section headers and
          should not be part of the requirement spec itself.

    Move requirements in ``install_requires`` that are using environment
    markers ``extras_require``.
    """

    # divide the install_requires into two sets, simple ones still
    # handled by install_requires and more complex ones handled by extras_require.

    inst_reqs = list(_reqs.parse(install_requires))
    simple_reqs = filter(_no_marker, inst_reqs)
    complex_reqs = filterfalse(_no_marker, inst_reqs)
    simple_install_requires = list(map(str, simple_reqs))

    for r in complex_reqs:
        extras_require[':' + str(r.marker)].setdefault(r)

    expanded_extras = dict(
        # list(dict.fromkeys(...))  ensures a list of unique strings
        (k, list(dict.fromkeys(str(r) for r in map(_clean_req, v))))
        for k, v in extras_require.items()
    )

    return simple_install_requires, expanded_extras


def _suffix_for(req):
    """Return the 'extras_require' suffix for a given requirement."""
    return ':' + str(req.marker) if req.marker else ''


def _clean_req(req):
    """Given a Requirement, remove environment markers and return it"""
    r = Requirement(str(req))  # create a copy before modifying
    r.marker = None
    return r


def _no_marker(req):
    return not req.marker


def _write_requirements(stream, reqs):
    lines = yield_lines(reqs or ())

    def append_cr(line):
        return line + '\n'

    lines = map(append_cr, lines)
    stream.writelines(lines)


def write_requirements(cmd, basename, filename):
    dist = cmd.distribution
    data = io.StringIO()
    install_requires, extras_require = _prepare(
        dist.install_requires or (), dist.extras_require or {}
    )
    _write_requirements(data, install_requires)
    for extra in sorted(extras_require):
        data.write('\n[{extra}]\n'.format(**vars()))
        _write_requirements(data, extras_require[extra])
    cmd.write_or_delete_file("requirements", filename, data.getvalue())


def write_setup_requirements(cmd, basename, filename):
    data = io.StringIO()
    _write_requirements(data, cmd.distribution.setup_requires)
    cmd.write_or_delete_file("setup-requirements", filename, data.getvalue())
