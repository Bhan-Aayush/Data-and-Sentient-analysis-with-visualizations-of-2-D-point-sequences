import pytest

from a3_part4 import load_data
from a3_ffwi_system import WeatherMetrics, FfwiOutput

import a3_ffwi_system as ffwi


class TestCalculateMr:
    """A collection of unit tests for calculate_mr."""

    def test_equation_3a_branch(self) -> None:
        """Test the branch calculate_mr that contains Equation 3a."""
        assert ffwi.calculate_mr(1.0, 150.0) <= 157.89521538860947

    def test_equation_3b_branch(self) -> None:
        """Test the branch calculate_mr that contains Equation 3b."""
        assert ffwi.calculate_mr(1.0, 150.000000000001) > 157.89521538860947


class TestCalculateM:
    """A collection of unit tests for calculate_m."""

    def test_no_mutation_mo_equals_ed(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo == ed."""
        wm = WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)
        ffwi.calculate_m(wm, 1.0, 1.0)

        assert wm == WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)

    def test_no_mutation_mo_leq_ew(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo <= ew."""
        wm = WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)
        ffwi.calculate_m(wm, 2.0, 1.0)

        assert wm == WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)

    def test_no_mutation_mo_greater_than_ew(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo > ew."""
        wm = WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)
        ffwi.calculate_m(wm, 2.0, 1.5)

        assert wm == WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)

    def test_no_mutation_mo_greater_than_ed(self) -> None:
        """Test that calculate_m does not mutate the WeatherMetrics argument when mo > ed."""
        wm = WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)
        ffwi.calculate_m(wm, 1.0, 2.0)

        assert wm == WeatherMetrics(1, 1, 1.0, 1.0, 1.0, 1.0)


@pytest.fixture
def sample_data() -> tuple[list[WeatherMetrics], list[FfwiOutput]]:
    """A pytest fixture containing the data in data/ffwi/sample_data.csv

    NOTE: Do not change this function. Do not call this function directly. It is a pytest fixture,
    so pytest will call it automatically and pass it to test_ffmc_against_ground_truth below.
    """
    return load_data('data/ffwi/sample_data.csv')


def test_ffmc_against_ground_truth(sample_data) -> None:
    """Test the correctness of calculate_ffmc, calculate_dmc, calculate_dc, calculate_isi,
     calculate_bui, and calculate_fwi based on sample_data.

    Ensure that, for every WeatherMetric element in sample_data[0] passed to each of the calculate_
    functions mentioned above, the return value, rounded to the nearest decimal, matches the
    corresponding value from the FfwiOutput element in sample_data[1].

    Hints:
        - You will need to use the built-in function round.
        - You may want to use pytest.approx since you are comparing float values.
    """
    ffmc = ffwi.INITIAL_FFMC
    dmc = ffwi.INITIAL_DMC
    dc = ffwi.INITIAL_DC

    inputs, outputs = sample_data
    ffmc_list = [ffwi.calculate_ffmc(x, ffmc) for x in inputs]
    dmc_list = [ffwi.calculate_dmc(x, dmc) for x in inputs]
    dc_list = [ffwi.calculate_dc(x, dc) for x in inputs]
    isi_list = [ffwi.calculate_isi(x, y) for x in inputs for y in ffmc_list]
    bui_list = [ffwi.calculate_bui(x, y) for x in dmc_list for y in dc_list]
    fwi_list = [ffwi.calculate_fwi(x, y) for x in isi_list for y in bui_list]

    for i in range(len(ffmc_list)):
        assert round(ffmc_list[i]) == pytest.approx(outputs[i].ffmc)
        assert round(dmc_list[i]) == pytest.approx(outputs[i].dmc)
        assert round(dc_list[i]) == pytest.approx(outputs[i].dc)
        assert round(isi_list[i]) == pytest.approx(outputs[i].isi)
        assert round(bui_list[i]) == pytest.approx(outputs[i].bui)
        assert round(fwi_list[i]) == pytest.approx(outputs[i].fwi)


if __name__ == '__main__':
    pytest.main(['a3_part4_tests.py'])
