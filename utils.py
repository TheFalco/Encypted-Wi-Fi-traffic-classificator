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


def open_pcapng(filename, folder, given_filter=None):
    """
    Open a pcapng file given its name and it containing folder
    :param filename: name of the file to be opened
    :param folder: relative path of the folder containing the file to open
    :param given_filter: wireshark optional display filter to be applied
    """
    result_path = os.path.join(pathlib.Path(__file__).parent.absolute(), folder)
    my_path = os.path.join(result_path, filename)
    return pyshark.FileCapture(my_path, display_filter=given_filter)
