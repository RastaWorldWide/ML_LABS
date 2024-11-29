import subprocess
import argparse


def main():
    parser = argparse.ArgumentParser(description="Download, process and upload data to S3")
    parser.add_argument('--bucket', required=True, help="S3 bucket name")
    parser.add_argument('--file', required=True, help="S3 file name")
    parser.add_argument('--local-dir', required=True, help="Local directory to store the data")

    args = parser.parse_args()

    local_file = f"{args.local_dir}/{args.file}"
    subprocess.run(
        ['python', 'download_data.py', '--bucket', args.bucket, '--file',
         args.file, '--local-path', local_file])

    processed_file = f"{args.local_dir}/processed_{args.file}"
    subprocess.run(['python', 'process_data.py', '--input',
                    local_file, '--output', processed_file])

    subprocess.run(
        ['python', 'upload_data.py', '--bucket',
         args.bucket, '--file', f'processed_{args.file}', '--local-path',
         processed_file])


if __name__ == '__main__':
    main()
