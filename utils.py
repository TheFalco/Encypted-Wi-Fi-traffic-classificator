from typing import List

import numpy as np
import pyshark
import pathlib
import json
import os


def open_json(filename, folder):
    """
    Open a json file given its name and its containing folder
    :param filename: name of the file to be opened
    :param folder: relative path of the folder containing the file to open
    """
    result_path = os.path.join(pathlib.Path(__file__).parent.absolute(), folder)
    my_path = os.path.join(result_path, filename)
    with open(my_path) as json_file:
        return json.load(json_file)


def open_pcapng(filename, folder):
    """
    Open a pcapng file given its name and it containing folder
    :param filename: name of the file to be opened
    :param folder: relative path of the folder containing the file to open
    """
    result_path = os.path.join(pathlib.Path(__file__).parent.absolute(), folder)
    my_path = os.path.join(result_path, filename)
    return pyshark.FileCapture(my_path)


def get_activities(data):
    """
    Find all the activities available in the reference file
    :param data: the reference file
    :return: a list of activities
    """
    activities = []
    for d in data:
        activities.append(d)
    return activities


def get_reference_values(data, activities):
    """
    Find the all the referenced value of the activities
    :param data: the reference file
    :param activities: the list of activities
    :return: a list of tuple (frame size, data rate) ordered by activity
    """
    values = []
    for a in activities:
        temp = []
        for i in range(len(data[a])):
            temp.append(list(data[a].values())[i])
        values.append(tuple(temp))
    return values


def load_tr_data(frame_size: List[int], activity: str, feature_set, feature_label, DELIM: int):
    """
    Load the training set list with the extrapolated data
    :param frame_size: up_frame_size or down_frame_size
    :param data_rate: up_data_rate or down_data_rate
    :param activity: name of the training file
    :param feature_set: up_features or down_features
    :param feature_label: up_labels or down_labels
    :param DELIM: size deliminator
    :return: the feature set, the label set and two empty lists, in order to clean up/down frame_size and data_rate
    """
    # feature_set is (mean frame size, mean data rate, percentage of packets with size < DELIM
    feature_set.append([np.mean(frame_size), np.std(frame_size),
                        (sum(i < DELIM for i in frame_size) / len(frame_size))])
    # feature_labels is index of file (will be useful to retrieve activity name)
    feature_label.append(activity)
    # Reset variables
    return feature_set, feature_label, [], []


def get_activity_name(activity: str) -> str:
    """
    Returns the name of the activity
    :param activity: name of training set files (ActivityName_XX)
    :return: the name of the activity
    """
    return activity[0:-3]
