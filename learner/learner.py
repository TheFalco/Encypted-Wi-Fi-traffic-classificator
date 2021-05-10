from sklearn.neighbors import KNeighborsClassifier
from tqdm import tqdm
import pickle
import utils

# Open input variables
data = utils.open_json("input_data.json", "config")

# Global variables
STA = data["STA"]
AP = data["AP"]
MAX = data["group_size"]
P = data["percentile"]
cap_len = data["capture_length"]

# List of training sample files
in_files = data["training_set"]


def train():
    """
    Train the model starting from the given training set
    :return: the trained model
    """
    # Learner variables
    features = []
    labels = []

    # Temp variables
    frame_size = []
    interval_time = []

    # Start learning from given data
    for f in in_files:
        print("Opening file %d/%d" % (in_files.index(f) + 1, len(in_files)))
        # Clean counters
        count = 1
        activity = utils.get_activity_name(f)

        # Open training file
        cap = utils.open_pcapng(f + ".pcapng", "training_captures")
        print("Analyzing...")
        # Initialize progress bar
        p_bar = tqdm(total=(cap_len[in_files.index(f)]//MAX), ncols=100, colour='white')

        for pck in cap:
            # To avoid malformed packets
            try:
                # Downstream
                if pck.wlan.da == STA and pck.wlan.sa == AP:
                    count += 1
                    frame_size.append(float(pck.frame_info.len))
                    interval_time.append(float(pck.frame_info.time_delta_displayed))
                    if count % MAX == 0:
                        features, labels, frame_size, interval_time = utils.load_tr_data(frame_size, activity, features,
                                                                                         labels, P, interval_time)
                        # Update progress bar
                        p_bar.update(1)
            except:
                # print("", end="")
                pass

        # Close the file and progress bar
        cap.close()
        p_bar.close()
        print("Closing file %d" % (in_files.index(f) + 1))

    print("Training the learner...")
    model = KNeighborsClassifier(n_neighbors=3)
    # Train the model using the training sets
    model.fit(features, labels)
    print("Done!")
    save_model(model)
    return model


def save_model(model):
    """
    Save the model in memory, for future uses
    :param model: the trained model
    """
    # Save the model to disk
    filename = './trained_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    print("Models correctly saved")


def load_ml_model():
    """
    Load the model from memory, if available. Otherwise, train the model
    :return: the trained model
    """
    try:
        print("Loading trained model...")
        learned_model = pickle.load(open("learner/trained_model.sav", "rb"))
        print("Done")
        return learned_model
    except (OSError, IOError):
        # If not present, start the learning
        print("Trained model not found.\nInitializing learner.py...")
        return train()
