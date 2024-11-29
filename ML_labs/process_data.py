import pandas as pd
import argparse


def process_data(input_file, output_file):
    df = pd.read_csv(input_file)

    df['processed'] = df['price'] * 1.1  # Увеличим цены на 10%

    df.to_csv(output_file, index=False)
    print(f"Processed data saved to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="Process data")
    parser.add_argument('--input', required=True, help="Input file path")
    parser.add_argument('--output', required=True, help="Output file path")

    args = parser.parse_args()
    process_data(args.input, args.output)


if __name__ == '__main__':
    main()
