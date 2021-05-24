from learner.learner import load_ml_model
import numpy as np
import pyshark

P = 300


def classify_online(sta: str, ap: str, interface: str, to: int):
    """
    Perform an online classification
    :param to: time_out of the capture; default is 20
    :param sta: station MAC address
    :param ap: access point MAC address
    :param interface: interface to listen on
    """
    # Load the model
    model = load_ml_model()
    # Set the filter
    capt_filter = "wlan.sa == " + ap + " && wlan.da == " + sta + " && wlan.fc.type_subtype == 0x0028"

    # Temp variables
    frame_size = []
    interval_time = []

    while True:
        print("Listening for " + str(to) + " seconds...")
        capture = pyshark.LiveCapture(interface=interface.lower(), display_filter=capt_filter)
        capture.sniff(timeout=to)

        print("Starting online analysis...")

        for pck in capture._packets:
            frame_size.append(int(pck.frame_info.len))
            interval_time.append(float(pck.frame_info.time_delta_displayed))
        # Calculate the mean of the sniffed data
        to_predict = [np.mean(frame_size), np.std(frame_size), (sum(i < P for i in frame_size) / len(frame_size)),
                      np.mean(interval_time)]
        print("Current user activity : " + model.predict([to_predict])[0])
