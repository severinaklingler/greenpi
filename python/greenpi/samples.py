import argparse
from samples.read_moisture import MoistureSample
from samples.read_temp_and_humidity import TemperatureSample


def build_argument_parser():
    parser = argparse.ArgumentParser(description='Run sample programs')
    parser.add_argument('-m', dest='mode', choices=['moisture','temperature'])
    return parser


if __name__ == "__main__":
    parser = build_argument_parser()   
    args = parser.parse_args()
    if args.mode == 'moisture':
        sample = MoistureSample()
        sample.run()
    if args.mode == 'temperature':
        sample = TemperatureSample(17)
        sample.run()
