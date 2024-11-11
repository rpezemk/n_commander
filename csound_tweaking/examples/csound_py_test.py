import subprocess

# Path to your .csd file
csd_file = "/home/przemek/n_commander/csound_tweaking/instruments/test_instrument.csd"

# Start Csound as a subprocess
process = subprocess.Popen(["csound", csd_file], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# Capture stdout and stderr if needed
stdout, stderr = process.communicate()

# Print Csound output
print(stdout.decode())
print(stderr.decode())
