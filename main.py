import argparse
import os

from alpha_vantage_runner import AplhaAdvantageRunner
from constants import DEFAULT_OUTPUT_FOLDER


def get_arg_parser():
    arg_parser = argparse.ArgumentParser(description='Alpa Vantage app')
    arg_parser.add_argument('-k',
                            '--api-key',
                            type=str,
                            required=True,
                            help="apikey for alpha vantage api, if you don't have one, you can claim your apikey on:\n"
                                 "https://www.alphavantage.co/support/#api-key")
    arg_parser.add_argument('-f',
                            '--output-format',
                            type=str,
                            default='json',
                            choices=['json', 'csv'],
                            help="For Alpha Vantage timeseries apis only, specify `datatype`;\n"
                                 "`json`, returns the api result in JSON format\n"
                                 "`csv`, returns the api result as a CSV file.")
    arg_parser.add_argument('-s',
                            '--output-size',
                            type=str,
                            default='compact',
                            choices=['compact', 'full'],
                            help="Some Alpha Vantage apis specify `outputsize`;\n"
                                 "`compact`, returns only the latest 100 data points'\n"
                                 "`full`, returns the full-length of the data.\n"
                                 "The `compact` option is recommended if you would like to reduce the data size of "
                                 "each API call.")
    arg_parser.add_argument('-d',
                            '--output-folder',
                            type=str,
                            required=False,
                            help="Provide a full path directory to use as a base to store output results when available"
                                 " (either json or csv).\n"
                                 "If not provided, will use `./output as a default.")

    arg_parser.add_argument('-v',
                            '--verbose',
                            action='store_true',
                            help="Print the output to the console of json apis in the console.")

    return arg_parser.parse_args()


if __name__ == "__main__":
    args = get_arg_parser()
    api_key = args.api_key
    output_format = args.output_format
    output_size = args.output_size
    output_dest = args.output_folder

    if output_dest:
        if not os.path.isdir(output_dest):
            raise FileNotFoundError('The provided directory does not exist.')
    else:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        output_dest = os.path.join(dir_path, DEFAULT_OUTPUT_FOLDER)
        if not os.path.isdir(output_dest):
            os.mkdir(output_dest)

    av_runner = AplhaAdvantageRunner(api_key=api_key, output_format=output_format, output_size=output_size,
                                     output_dest=output_dest, verbose=args.verbose)
    av_runner.run()
