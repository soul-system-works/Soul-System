"""THE timing constants. Nothing else in the pipeline may hard-code a duration.

Holds are computed from these, not authored: the storyboard carries content and
order, the linter carries the arithmetic. An explicit `hold` may only raise a
scene above its computed minimum, never lower it. See docs/video-pipeline.md.
"""

BASE_HOLD       = 1.5    # s — every scene, before any text
WORD_RATE       = 0.35   # s per word of prose (headings, bullets, outro)
CODE_BASE       = 1.0    # s — extra settle time for code/terminal scenes
CODE_LINE_RATE  = 0.6    # s per visible code/terminal line
TRANSITION_DUR  = 0.4    # s (fade); cut = 0. Not counted against hold
MAX_WORDS_SCENE = 26     # one-idea-per-scene proxy (prose scenes)
MAX_BULLETS     = 4      # per bullets scene
MAX_CODE_LINES  = 12     # per code/terminal scene
BUDGET_SKILL    = 60.0   # s — hard lint failure
BUDGET_OVERVIEW = 180.0  # s — hard lint failure
