import argparse


def register_launch_arguments():
    parser = argparse.ArgumentParser(description='Serve the app')
    parser.add_argument('-i', '--input', help='specify input file', required=True)
    parser.add_argument('-o', '--output', help='specify output file', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = register_launch_arguments()
