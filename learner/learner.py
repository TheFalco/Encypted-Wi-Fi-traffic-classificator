from sklearn.neighbors import KNeighborsClassifier
import pickle
import utils

# Open input variables
data = utils.open_json("input_data.json", "config")

# Global variables
STA = data["STA"]
AP = data["AP"]
MAX = data["group_size"]
DELIM = data["percentile"]

# List of training sample files
in_files = data["training_set"]


def train():
    # Learner variables
    up_features = []
    up_labels = []
    down_features = []
    down_labels = []

    # Temp variables
    up_frame_size = []
    down_frame_size = []

    # Start learning from given data
    for f in in_files:
        print("Opening file %d/%d" % (in_files.index(f) + 1, len(in_files)))
        # Clean counters
        up_count = 1
        down_count = 1
        activity = utils.get_activity_name(f)

        # Open training file
        cap = utils.open_pcapng(f + ".pcapng", "training_captures")

        print("Analyzing...")
        for pck in cap:
            # To avoid malformed packets
            try:
                # Upstream
                if pck.wlan.da == AP and pck.wlan.sa == STA:
                    up_frame_size.append(int(pck.frame_info.len))
                    up_count += 1
                    if up_count % MAX == 0:
                        up_features, up_labels, up_frame_size, up_data_rate = \
                            utils.load_tr_data(up_frame_size, activity,
                                               up_features, up_labels, DELIM)
                # Downstream
                elif pck.wlan.da == STA and pck.wlan.sa == AP:
                    down_count += 1
                    down_frame_size.append(float(pck.frame_info.len))
                    if down_count % MAX == 0:
                        down_features, down_labels, down_frame_size, down_data_rate = \
                            utils.load_tr_data(down_frame_size, activity,
                                               down_features, down_labels, DELIM)
            except:
                # print("", end="")
                pass

        # Close the file
        cap.close()
        print("Closing file %d" % (in_files.index(f) + 1))

    print("Training the learner...")
    # up_model = KNeighborsClassifier(n_neighbors=3)
    down_model = KNeighborsClassifier(n_neighbors=3)
    # Train the model using the training sets
    # up_model.fit(up_features, up_labels)
    down_model.fit(down_features, down_labels)
    print("Done!")
    save_model(down_model)
    return down_model


def save_model(down_model):
    # Save the model to disk
    filename = 'learner/trained_model.sav'
    # to_save_tuple = (up_model, down_model)
    pickle.dump(down_model, open(filename, 'wb'))
    print("Models correctly saved")


def load_ml_model():
    try:
        print("Loading trained models...")
        # up_lrnd_model,
        down_lrnd_model = pickle.load(open("learner/trained_model.sav", "rb"))
        print("Done")
        return down_lrnd_model
    except (OSError, IOError) as e:
        # If not present, start the learning
        print("Trained models not found.\nInitializing learner.py...")
        return train()
