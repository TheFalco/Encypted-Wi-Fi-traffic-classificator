import pyshark
from learner.learner import load_ml_model
import numpy as np

# Global variables
P = 300


def classify_offline(path: str, sta: str, ap: str):
    """
    Analyze the given file
    :param path: path to the file
    :param sta: station MAC address
    :param ap: access point MAC address
    """
    # Variables
    frame_size = []
    interval_time = []

    # try to load the model, otherwise create a new one
    learned_model = load_ml_model()

    # Open file to classify_offline
    cap = pyshark.FileCapture(path)

    print("Starting offline analysis...")

    # Extrapolate the data from the file
    for pck in cap:
        # We need to manage malformed packets
        try:
            if pck.highest_layer == 'DATA':
                # Downstream
                if pck.wlan.da == sta and pck.wlan.sa == ap:
                    frame_size.append(int(pck.frame_info.len))
                    interval_time.append((float(pck.frame_info.time_delta_displayed)))
        except:
            # print("", end="")
            pass
    cap.close()

    # Calculate the mean of the extrapolated data
    to_predict = [np.mean(frame_size), np.std(frame_size), (sum(i < P for i in frame_size) / len(frame_size)),
                  np.mean(interval_time)]
    # Predict the model
    predict(learned_model, to_predict)


def predict(model, capture):
    """
    Run the prediction
    :param model: the trained model
    :param capture: the analyzed offline model
    """
    # Run the prediction
    result = model.predict([capture])

    print(result)
    print("Analysis completed: ", end=" ")
    print(result[0])
