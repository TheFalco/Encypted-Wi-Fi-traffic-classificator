import utils
import pickle
from learner.learner import load_ml_model
from sklearn.metrics import plot_confusion_matrix
import matplotlib.pyplot as plt
from tqdm import tqdm


def compute_test_set():
    data = utils.open_json("input_data.json", "config")

    # Global variables
    sta = data["STA"]
    ap = data["AP"]
    g_size = 500
    p = data["percentile"]
    cap_len = data["capture_length"]

    # List of training sample files
    in_files = data["training_set"]

    to_predict = []
    labels = []
    frame_size = []
    interval_time = []

    for f in in_files:
        # Clean counters
        count = 1
        activity = utils.get_activity_name(f)
        print("Evaluating file: %s" % f)
        cap = utils.open_pcapng(f + ".pcapng", "training_captures")
        p_bar = tqdm(total=(cap_len[in_files.index(f)] // g_size), ncols=100, colour='white', desc='Analyzing')
        for pck in cap:
            # To avoid malformed packets
            try:
                # Downstream
                if pck.wlan.da == sta and pck.wlan.sa == ap:
                    count += 1
                    frame_size.append(float(pck.frame_info.len))
                    interval_time.append(float(pck.frame_info.time_delta_displayed))
                    if count % g_size == 0:
                        to_predict, labels, frame_size, interval_time = utils.load_tr_data(frame_size, activity,
                                                                                           to_predict,
                                                                                           labels, p, interval_time)
                        p_bar.update(1)
            except:
                # print("", end="")
                pass
        p_bar.close()
        cap.close()

    anal_file = 'learner/evaluation_file.sav'
    pickle.dump((to_predict, labels), open(anal_file, 'wb'))
    return to_predict, labels


def evaluate_model():
    model = load_ml_model()
    try:
        print("Loading pre-processed test dataset...")
        to_predict, labels = pickle.load(open('learner/evaluation_file.sav', 'rb'))
        print("...loading succeeded")
    except:
        print("...loading failed, processing test dataset")
        to_predict, labels = compute_test_set()

    print("Computing confusion matrix...")
    plot_confusion_matrix(model, to_predict, labels, cmap=plt.cm.Blues)
    print("...matrix computed")
    plt.savefig('learner/confusion_matrix.png')
    plt.show()

