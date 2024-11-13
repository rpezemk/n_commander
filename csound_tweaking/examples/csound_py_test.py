import subprocess
from typing import Any

# Path to your .csd file
def run_example(sth: Any):
    csd_file = "/home/przemek/n_commander/csound_tweaking/instruments/test_instrument.csd"
    process = subprocess.Popen(["csound", csd_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
if __name__ == "__main__":
    run_example()
    
def run_example_2():
    csd_file = "/home/przemek/n_commander/csound_tweaking/instruments/test_instrument.csd"
    process = subprocess.Popen(["csound", csd_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
if __name__ == "__main__":
    run_example()