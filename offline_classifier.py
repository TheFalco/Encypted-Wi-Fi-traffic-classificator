import pyshark

import utils
from learner.learner import load_ml_model
import numpy as np

# Global variables
DELIM = 300


def classify(path: str, sta: str, ap: str):
    # Variables
    up_frame_size = []
    down_frame_size = []

    # try to load the model, otherwise create a new one
    down_lrnd_model = load_ml_model()

    # Open file to classify
    cap = pyshark.FileCapture(path)

    print("Starting offline analysis...")

    # Extrapolate the data from the file
    for pck in cap:
        # We need to manage malformed packets
        try:
            if pck.highest_layer == 'DATA':
                # Upstream
                if pck.wlan.da == ap and pck.wlan.sa == sta:
                    up_frame_size.append(int(pck.frame_info.len))
                # Downstream
                elif pck.wlan.da == sta and pck.wlan.sa == ap:
                    down_frame_size.append(int(pck.frame_info.len))
        except:
            # print("", end="")
            pass
    cap.close()

    # Calculate the mean of the extrapolated data
    # to_predict_up = [np.mean(up_frame_size), np.std(up_frame_size),
    #                  (sum(i < DELIM for i in up_frame_size) / len(up_frame_size))]
    to_predict_down = [np.mean(down_frame_size), np.std(down_frame_size),
                       (sum(i < DELIM for i in down_frame_size) / len(down_frame_size))]

    predict(down_lrnd_model, to_predict_down)


def predict(model, capture):
    # Run the prediction
    # result_up = up_lrnd_model.predict([to_predict_up])
    result_down = model.predict([capture])

    print(result_down)
    print("Analisys complited: ", end=" ")
    print(result_down[0])
