import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import serial
import yaml
from collections import deque
from time import sleep, perf_counter
import main

def collect_data(collection_time=5):
    with open("config.yaml", "r") as file:
        config = yaml.safe_load(file)

    port = config["port"]
    mapping = config["slider_mapping"]
    max_slider_value = config["max_slider_value"]
    baud_rate = config["baud_rate"]

    data = deque()

    with serial.Serial(port, baud_rate) as ser:
        start_time = perf_counter()
        end_time = start_time + collection_time
        while(perf_counter() < end_time):
            data.append(int(ser.readline().decode("ascii")))
    data = np.array(list(data))
    x = np.linspace(start=0, stop=collection_time, num=len(data))
    return data


if __name__ == "__main__":
    data = collect_data()
    x = np.linspace(0, 1, len(data))
    plt.plot(x, data, "o")
    plt.show()

