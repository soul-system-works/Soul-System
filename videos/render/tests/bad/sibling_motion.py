"""Negative fixture: a builder that splits itself across two files."""

from helper_lib import GREETING


def build(scene, theme, components, duration):
    components.kinetic_line(scene, [GREETING], duration=duration)
