#!/usr/bin/env python
import os
import argparse


import os
import argparse

def concatenate_files(path, suffix):
    result = ""
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(suffix):
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    result += f"\n\n\n=== {file_path} ===\n"
                    result += f.read()
                    result += "\n"
    return result

def main():
    parser = argparse.ArgumentParser(description='Concatenate files with a specific suffix.')
    parser.add_argument('path', type=str, help='the path of the directory to search')
    parser.add_argument('suffix', type=str, help='the suffix of the files to concatenate')

    args = parser.parse_args()

    print(concatenate_files(args.path, args.suffix))

if __name__ == "__main__":
    main()
