from online_classifier import classify_online
from offline_classifier import classify_offline
from learner.model_evaluation import evaluate_model
import argparse


def start():
    parser = argparse.ArgumentParser()

    parser.add_argument("-f", default="", type=str, required=False)
    parser.add_argument("-sta", default="", type=str, required=True)
    parser.add_argument("-ap", default="", type=str, required=True)
    parser.add_argument("-type", default=0, type=int, required=True)
    parser.add_argument("-i", default="", type=str, required=False)
    parser.add_argument("-t", default="20", type=int, required=False)

    args = parser.parse_args()

    sta = args.sta
    ap = args.ap

    if args.type == 1:
        # start online capture
        classify_online(sta, ap, args.i, args.t)
    elif args.type == 0:
        # start offline capture
        classify_offline(args.f, sta, ap)
    elif args.type == 2:
        evaluate_model()


if __name__ == "__main__":
    start()
