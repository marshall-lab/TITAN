import pytest
import os

import titan.probabilities as probs


@pytest.mark.unit
def test_safe_sex():
    year_steps = 12
    # initiate result dict with 2 time steps
    assert probs.safe_sex(0, year_steps) == 0.443
    assert probs.safe_sex(1, year_steps) == 0.481
    assert probs.safe_sex(5, year_steps) == 0.514
    assert probs.safe_sex(100, year_steps) == 0.759


@pytest.mark.unit
def test_adherence_prob():
    # initiate result dict with 2 time steps
    assert probs.adherence_prob(1) == 0.0051
    assert probs.adherence_prob(2) == 0.0039
    assert probs.adherence_prob(3) == 0.0032
    assert probs.adherence_prob(4) == 0.0025
    assert probs.adherence_prob(5) == 0.0008
    assert probs.adherence_prob(6) == 0.0051


@pytest.mark.unit
def test_get_death_rate(params):
    for hiv in [True, False]:
        for aids in [True, False]:
            for race in ["WHITE", "BLACK"]:
                for adh in [0, 1]:
                    assert (
                        probs.get_death_rate(
                            hiv,
                            aids,
                            race,
                            adh,
                            params.demographics[race].death_rate,
                            params.model.time.steps_per_year,
                        )
                        > 0
                    )
