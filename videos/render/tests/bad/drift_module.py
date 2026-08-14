"""Negative fixture: a builder that does not give its slot back.

Deliberately spends its whole allotment and then half a second more, so the
smoke test can prove render.py refuses to publish a timings.json it would have
made wrong.
"""

OVERRUN = 0.5   # s past the slot


def overrun(scene, theme, components, duration):
    components.kinetic_line(scene, ["Takes more than", "it was given."],
                            duration=duration)
    scene.wait(components.hold_time(components.frames_for(OVERRUN)),
               frozen_frame=True)
