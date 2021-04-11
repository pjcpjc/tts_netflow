import os
import inspect
import tts_netflow
import unittest

def _this_directory() :
    return os.path.dirname(os.path.realpath(os.path.abspath(inspect.getsourcefile(_this_directory))))

def get_test_data(data_set_name):
    path = os.path.join(_this_directory(), "data", data_set_name)
    assert os.path.exists(path), f"bad path {path}"
    # right now assumes data is archived as either a directory of csv files or a single json file for each data set
    if os.path.isfile(path):
        return tts_netflow.input_schema.json.create_tic_dat(path)
    return tts_netflow.input_schema.csv.create_tic_dat(path)

def _nearly_same(x, y, epsilon=1e-5):
    if x == y or max(abs(x), abs(y)) < epsilon:
        return True
    if min(abs(x), abs(y)) > epsilon:
        return abs(x-y) /  min(abs(x), abs(y)) < epsilon

def _smaller(x, y, epsilon=1e-5):
    return x < y and not _nearly_same(x, y, epsilon)

class TestNetflow(unittest.TestCase):
    # This is a pretty simple test suite - just two data sets. But the template should be clear for how you could
    # archive many useful data sets for validating your optimization engine.
    def test_standard_data_set(self):
        dat = get_test_data("sample_data.json")
        sln = tts_netflow.solve(dat)
        self.assertTrue(_nearly_same(5500.0, sln.parameters["Total Cost"]["Value"], epsilon=1e-4))


    def test_sloan_data_set(self):
        # This data set was pulled from this MIT Sloan School of Management example problem here https://bit.ly/3254VpT
        dat = get_test_data("sloan_data_set.json")
        sln = tts_netflow.solve(dat)
        self.assertTrue({k: v["Quantity"] for k,v in sln.flow.items()} ==
            {(2, 3, 2): 2.0,
             (2, 2, 5): 2.0,
             (2, 5, 6): 2.0,
             (1, 1, 2): 3.0,
             (1, 2, 5): 3.0,
             (1, 5, 4): 3.0,
             (1, 1, 4): 2.0})

# Run the tests via the command line
if __name__ == "__main__":
    unittest.main()