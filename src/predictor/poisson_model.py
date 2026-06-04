from math import exp
from math import factorial


def poisson_probability(
    goals,
    expected_goals
):

    return (
        (
            expected_goals ** goals
        )
        * exp(-expected_goals)
        / factorial(goals)
    )

def most_likely_goals(
    expected_goals,
    max_goals=6
):

    probabilities = {}

    for goals in range(
        max_goals + 1
    ):

        probabilities[goals] = (
            poisson_probability(
                goals,
                expected_goals
            )
        )

    return max(
        probabilities,
        key=probabilities.get
    )