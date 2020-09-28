import argparse
import json

from dcel import DCEL, Point
from slab import SearchSystem


def register_launch_arguments():
    parser = argparse.ArgumentParser(description='Serve the app')
    parser.add_argument('-i', '--input', help='specify input file', required=True)
    parser.add_argument('-o', '--output', help='specify output file', required=True)
    return parser.parse_args()


if __name__ == '__main__':
    args = register_launch_arguments()

    try:
        with open(args.input) as input_file:
            input_data = json.load(input_file)
        dcel = DCEL(**input_data['pslg'])
        points = [Point(**point_dict) for point_dict in input_data['points']]
        search_system = SearchSystem(dcel)
        output_data = {'faces': [search_system.locate_point(point) for point in points]}
    except FileNotFoundError as e:
        output_data = {'error': f"No such file '{e.filename}'"}
    except (json.decoder.JSONDecodeError, KeyError):
        output_data = {'error': 'Incorrect file format'}
    except IndexError:
        output_data = {'error': 'Incorrect indexing'}
    except Exception as e:
        output_data = {'error': str(e)}

    with open(args.output, 'w') as output_file:
        json.dump(output_data, output_file, indent=2)
