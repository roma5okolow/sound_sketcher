import argparse
import numpy as np
from scipy.io import wavfile
from utils import signal_stretcher


def parse_args():
    desc = 'Stretch sound without changing the pitch.'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('input_path',
                        type=str,
                        help='Input path to wav file.')
    parser.add_argument('output_path',
                        type=str,
                        help='Output path to save modified wav file.')
    parser.add_argument('time_stretch_ratio',
                        type=float,
                        help='The signal will be stretched by ratio times.')
    return parser.parse_args()


def main():
    args = parse_args()
    fs, data = wavfile.read(args.input_path)

    # Handle multi-channel input
    if len(data.shape) != 1:
        data = data.mean(axis=1)

    # Normalization
    data = data.astype(float) / np.max(data)

    output = signal_stretcher(data, args.time_stretch_ratio)

    wavfile.write(args.output_path, fs, output)

    print(f'Duration of source file = {(len(data) / fs):.2f} s')
    print(f'Duration of modified file = {(len(output) / fs):.2f} s')
    print(f'Actual stretch = {(len(output) / len(data)):.2f} times')
    print(f'Result saved to {args.output_path}')


if __name__ == '__main__':
    main()