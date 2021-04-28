import numpy as np
import pyshark
from learner.learner import load_ml_model

DELIM = 300


def classify_online(sta: str, ap: str, interface: str):
    down_model = load_ml_model()
    capt_filter = "wlan.sa == " + ap + " && wlan.da == " + sta + " && wlan.fc.type_subtype == 0x0028"
    while True:
        capture = pyshark.LiveCapture(interface=interface.lower(), display_filter=capt_filter)
        capture.sniff(timeout=20)

        down_frame_size = [pck.frame_info.len for pck in capture]
        to_predict_down = [np.mean(down_frame_size), np.std(down_frame_size),
                           (sum(i < DELIM for i in down_frame_size) / len(down_frame_size))]
        print("Analysis completed: " + down_model.predict(to_predict_down)[0])
