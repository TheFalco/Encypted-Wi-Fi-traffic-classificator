import argparse
from offline_classifier import classify
from online_classifier import classify_online


def start():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", default="", type=str, required=False)
    parser.add_argument("-sta", default="", type=str, required=True)
    parser.add_argument("-ap", default="", type=str, required=True)
    parser.add_argument("-type", default="", type=int, required=True)
    parser.add_argument("-i", default="", type=str, required=False)

    args = parser.parse_args()

    sta = args.sta
    ap = args.ap

    if args.type:
        # start online capture
        classify_online(sta, ap, args.i)
    else:
        # start offline capture
        classify(args.f, sta, ap)


if __name__ == "__main__":
    start()
