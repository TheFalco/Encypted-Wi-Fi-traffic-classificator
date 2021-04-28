import utils
import pickle
import numpy as np


# Load the training data
try:
    print("Loading trained models...")
    up_lrnd_model, down_lrnd_model = pickle.load(open("learner/trained_model.sav", "rb"))
    print("Done")
except (OSError, IOError) as e:
    # If not present, start the learning
    print("Trained models not found.\nInitializing learner.py...")
    from learner.learner import down_model
    # up_lrnd_model = up_model
    down_lrnd_model = down_model

# Open input variables
data = utils.open_json("input_data.json", "config")

# Global variables
STA = data["STA"]
AP = data["AP"]
FILE = data["offline_file"]
DELIM = data["percentile"]

# Open file to classify
cap = utils.open_pcapng(FILE, "offline_captures")

# Variables
up_frame_size = []
avg_up_frame_size = 0
avg_up_data_rate = 0
down_frame_size = []
avg_down_frame_size = 0
avg_down_data_rate = 0

print("Starting offline analysis...")

# Extrapolate the data from the file
for pck in cap:
    # We need to manage malformed packets
    try:
        if pck.highest_layer == 'DATA':
            # Upstream
            if pck.wlan.da == AP and pck.wlan.sa == STA:
                up_frame_size.append(int(pck.frame_info.len))
            # Downstream
            elif pck.wlan.da == STA and pck.wlan.sa == AP:
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

# Run the prediction
# result_up = up_lrnd_model.predict([to_predict_up])
result_down = down_lrnd_model.predict([to_predict_down])

# TODO: Classification based on results
print(result_down)
print("Analisys complited: ", end=" ")
print(result_down[0])
