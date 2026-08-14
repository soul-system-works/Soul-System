# the linter owns this arithmetic, not taste
def computed_hold(words):
    return BASE_HOLD + WORD_RATE * words


def over_budget(scenes, budget):
    return sum(s.hold for s in scenes) > budget
