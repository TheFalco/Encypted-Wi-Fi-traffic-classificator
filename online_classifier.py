from learner.learner import load_ml_model
import numpy as np
import pyshark

P = 300


def classify_online(sta: str, ap: str, interface: str):
    """
    Perform an online classification
    :param sta: station MAC address
    :param ap: access point MAC address
    :param interface: interface to listen on
    """
    # Load the model
    down_model = load_ml_model()
    # Set the filter
    capt_filter = "wlan.sa == " + ap + " && wlan.da == " + sta + " && wlan.fc.type_subtype == 0x0028"

    print("Starting online analysis...")

    while True:
        print("Listening for 20 seconds...")
        capture = pyshark.LiveCapture(interface=interface.lower(), display_filter=capt_filter)
        capture.sniff(timeout=20)

        down_frame_size = [pck.frame_info.len for pck in capture]
        # Calculate the mean of the sniffed data
        to_predict_down = [np.mean(down_frame_size), np.std(down_frame_size),
                           (sum(i < P for i in down_frame_size) / len(down_frame_size))]
        print("Current user activity : " + down_model.predict(to_predict_down)[0])
