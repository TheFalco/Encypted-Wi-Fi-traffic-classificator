import argparse
from offline_classifier import classify


def start():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", default="", type=str, required=False)
    parser.add_argument("-sta", default="", type=str, required=True)
    parser.add_argument("-ap", default="", type=str, required=True)
    parser.add_argument("-type", default="", type=int, required=True)

    args = parser.parse_args()

    sta = args.sta
    ap = args.ap

    if args.type:
        # start online capture
        pass
    else:
        # start offline capture
        classify(args.f, sta, ap)


if __name__ == "__main__":
    start()
