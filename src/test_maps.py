import pytest
import subprocess
import pandas as pd
import numpy as np
import io

# needs -s flag when running with pytest
def test_cords_passed_correctly():
    mapRunner = subprocess.run(["python", "./maps.py"],universal_newlines=True,stdout=subprocess.PIPE)
    print(mapRunner.stdout)
    df = pd.read_csv("./maps_test.csv")
    df.head()

    mapOut=pd.read_csv(io.StringIO(mapRunner.stdout))
    mapOut.head()

    assert len(mapOut.Latitude)==len(df.Latitude)
    assert len(mapOut.Longitude)==len(df.Longitude)
    assert len(mapOut.Latitude)==len(df.Longitude)
    for x in range(0,len(mapOut.Latitude)):
        assert np.format_float_positional(mapOut.Latitude[x],precision=7,trim="k",unique=False) == np.format_float_positional(df.Latitude[x],precision=7,trim="k",unique=False)
        # pytest test_maps.py -s -rP
        # print(np.format_float_positional(mapOut.Latitude[x]) +":"+np.format_float_positional(df.Latitude[x]))
        # print(np.format_float_positional(mapOut.Longitude[x]) +":"+np.format_float_positional(df.Longitude[x]))
        assert np.format_float_positional(mapOut.Longitude[x],precision=7,trim="k",unique=False) == np.format_float_positional(df.Longitude[x],precision=7,trim="k",unique=False)

    print("The exit code was: %d" % mapRunner.returncode)