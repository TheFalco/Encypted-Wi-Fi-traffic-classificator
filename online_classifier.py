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
    model = load_ml_model()
    # Set the filter
    capt_filter = "wlan.sa == " + ap + " && wlan.da == " + sta + " && wlan.fc.type_subtype == 0x0028"

    print("Starting online analysis...")

    while True:
        print("Listening for 20 seconds...")
        capture = pyshark.LiveCapture(interface=interface.lower(), display_filter=capt_filter)
        capture.sniff(timeout=20)

        print("Starting online analysis...")
        
        frame_size = [int(pkt.frame_info.len) for pkt in capture._packets]
        # Calculate the mean of the sniffed data
        to_predict = [np.mean(frame_size), np.std(frame_size), (sum(i < P for i in frame_size) / len(frame_size))]
        print("Current user activity : " + model.predict([to_predict])[0])
