import pytest
import networkx as nx

import os
import subprocess
import csv
import math

from titan.parse_params import ObjMap, create_params
from titan.model import HIVModel


@pytest.fixture
def params(tmpdir):
    param_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "params", "simple_integration.yml"
    )
    return create_params(None, param_file, tmpdir)


@pytest.fixture
def make_model(params):
    def _make_model():
        return HIVModel(params)

    return _make_model


@pytest.mark.integration
def test_model_runs():
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "run_titan.py")
    param_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "params", "basic.yml"
    )

    subprocess.check_call([f, f"-p {param_file}"])
    assert True


@pytest.mark.integration
def test_model_reproducible(tmpdir):
    path_a = tmpdir.mkdir("result_a")
    path_b = tmpdir.mkdir("result_b")
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "run_titan.py")
    param_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "params", "basic_seeded.yml"
    )

    subprocess.check_call([f, f"-p {param_file}", f"-o {path_a}"])
    subprocess.check_call([f, f"-p {param_file}", f"-o {path_b}"])

    result_file_a = os.path.join(path_a, "basicReport_MSM_BLACK.txt")
    result_file_b = os.path.join(path_b, "basicReport_MSM_BLACK.txt")
    assert os.path.isfile(result_file_a)
    with open(result_file_a, newline="") as fa, open(result_file_b, newline="") as fb:
        reader_a = csv.DictReader(fa, delimiter="\t")
        res_a = []
        for row in reader_a:
            res_a.append(row)

        reader_b = csv.DictReader(fb, delimiter="\t")
        res_b = []
        for row in reader_b:
            res_b.append(row)

    for i in range(len(res_a)):
        assert res_a[i]["t"] == res_b[i]["t"]
        assert res_a[i]["run_id"] != res_b[i]["run_id"]
        assert res_a[i]["rseed"] == res_b[i]["rseed"]
        assert res_a[i]["pseed"] == res_b[i]["pseed"]
        assert res_a[i]["Total"] == res_b[i]["Total"]
        assert res_a[i]["HIV"] == res_b[i]["HIV"]
        assert res_a[i]["PrEP"] == res_b[i]["PrEP"]
        assert res_a[i]["Deaths"] == res_b[i]["Deaths"]
        assert res_a[i]["HIV"] == res_b[i]["HIV"]


@pytest.mark.integration
def test_model_settings_run(tmpdir):
    f = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "run_titan.py")
    param_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "params", "integration_base.yml"
    )

    for item in os.listdir(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "settings")
    ):
        if "__" not in item and item != "base":
            path = tmpdir.mkdir(item)
            subprocess.check_call([f, f"-p {param_file}", f"-o {path}", f"-S {item}"])
            assert True


@pytest.mark.integration
def test_target_partners(make_model, tmpdir):
    """
    If we increase the number of target partners, does the number of actual partners increase?
    """
    model_a = make_model()
    model_a.params.outputs.network.edge_list = True

    path_a = tmpdir.mkdir("a")
    path_a.mkdir("network")
    path_b = tmpdir.mkdir("b")
    path_b.mkdir("network")

    # run with default bins (0-9)
    run_id_a = model_a.run(path_a)

    # change the bins upward for creating model b
    bins = {
        15: {"prob": 0.3},
        20: {"prob": 0.4},
        25: {"prob": 0.3},
    }
    model_a.params.model.population.num_partners.bins = ObjMap(bins)

    model_b = HIVModel(model_a.params)

    run_id_b = model_b.run(path_b)

    g_a_0 = nx.read_edgelist(
        os.path.join(path_a, "network", f"{run_id_a}_Edgelist_t0.txt"),
        delimiter="|",
        data=False,
    )
    g_a_10 = nx.read_edgelist(
        os.path.join(path_a, "network", f"{run_id_a}_Edgelist_t10.txt"),
        delimiter="|",
        data=False,
    )
    g_b_0 = nx.read_edgelist(
        os.path.join(path_b, "network", f"{run_id_b}_Edgelist_t0.txt"),
        delimiter="|",
        data=False,
    )
    g_b_10 = nx.read_edgelist(
        os.path.join(path_b, "network", f"{run_id_b}_Edgelist_t10.txt"),
        delimiter="|",
        data=False,
    )

    # should be at least 2x bigger
    assert (g_a_0.number_of_edges() * 2) < g_b_0.number_of_edges()
    assert (g_a_10.number_of_edges() * 2) < g_b_10.number_of_edges()


@pytest.mark.integration
def test_prep_coverage(make_model, tmpdir):
    """
    If we increase the target of prep coverage, does the incidence of hiv decrease?
    """
    model_a = make_model()

    path_a = tmpdir.mkdir("a")
    path_b = tmpdir.mkdir("b")

    # run with default bins (0-9)
    run_id_a = model_a.run(path_a)

    # change the coverage upward for creating model b
    model_a.params.prep.target = 0.9

    model_b = HIVModel(model_a.params)

    run_id_b = model_b.run(path_b)

    result_file_a = os.path.join(path_a, "basicReport_ALL_ALL.txt")
    result_file_b = os.path.join(path_b, "basicReport_ALL_ALL.txt")
    assert os.path.isfile(result_file_a)
    with open(result_file_a, newline="") as fa, open(result_file_b, newline="") as fb:
        reader_a = csv.DictReader(fa, delimiter="\t")
        res_a = []
        for row in reader_a:
            res_a.append(row)

        reader_b = csv.DictReader(fb, delimiter="\t")
        res_b = []
        for row in reader_b:
            res_b.append(row)

    # at start, should be similar
    assert res_a[0]["t"] == res_b[0]["t"]
    assert math.isclose(
        float(res_a[0]["HIV"]), float(res_b[0]["HIV"]), rel_tol=0.3
    )  # within 30%
    assert int(res_a[0]["PrEP"]) < int(res_b[0]["PrEP"])

    # at end, should be different
    assert res_a[9]["t"] == res_b[9]["t"]
    assert not math.isclose(
        float(res_a[9]["HIV"]), float(res_b[9]["HIV"]), rel_tol=0.3
    )  # not within 30%
    assert int(res_a[9]["PrEP"]) < int(res_b[9]["PrEP"])
