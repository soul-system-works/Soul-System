"""Smoke fixture: a `custom` scene builder exercising all three primitives.

Not a shipping video — this exists so the renderer's custom path (import,
builder contract, exact-slot drift check) is covered by the smoke test. It is
also the worked example of the contract documented at the top of components.py:
every string it draws is declared in the storyboard's `text:`, and it closes its
own frame arithmetic against the slot it was given.
"""

# Timings the builder spends, in seconds. They are named so the arithmetic at
# the bottom reads as arithmetic and not as magic numbers.
LEAD_IN = 1.8      # kinetic_line
LIFELINE = 3.0     # thread, drawn with two marks
FLIGHT = 1.2       # fly_card into the file card
CLOSE = 0.5        # thread fades


def build(scene, theme, components, duration):
    total = components.frames_for(duration)

    components.kinetic_line(
        scene, ["The record", "outlives", "the session."],
        duration=LEAD_IN, y=2.2)

    record = components.file_card("witness.md").scale(0.8)
    record.move_to([3.4, -1.7, 0])
    scene.add(record)

    # No explicit width: the default has to be centre-safe WITH its label, so
    # the fixture renders the path a real storyboard will take.
    line = components.thread(
        scene, LIFELINE, y=0.0, label="session one",
        marks=[{"at": 0.35, "label": "capture", "persistent": True},
               {"at": 0.75, "label": "handoff"}])

    components.fly_card(scene, "idea", line.marks[0], record, FLIGHT)
    line.end(scene, CLOSE)

    spent = (components.frames_for(LEAD_IN) + components.frames_for(LIFELINE)
             + components.frames_for(FLIGHT) + components.frames_for(CLOSE))
    rest = total - spent
    if rest:
        scene.wait(components.hold_time(rest), frozen_frame=True)
