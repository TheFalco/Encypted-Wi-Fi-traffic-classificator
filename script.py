import utils
from statistics import mean

data = utils.open_json("input_data.json", "config")

# Global variables
STA = data["STA"]
AP = data["AP"]
FILE = data["pcapng_file"]

# Filter
cap_filter = "wlan.da == " + STA + " && wlan.sa == " + AP + " && wlan.fc.type_subtype == 0x0028"
cap = utils.open_pcapng(FILE, "captures", cap_filter)

# Variables
frame_len = []
delta_time = []
avg_frame_len = 0
avg_delta_time = 0

i = 0
for pck in cap:
    # We need to manage malformed packets
    try:
        frame_len.append(int(pck.frame_info.len))
        i += 1
        if i % 50 == 0:
            print(int(mean(frame_len)))

    except:
        print("", end="")
        pass
