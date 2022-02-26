import copy
import os
import argparse
import sys
import hashlib
from typing import List, Tuple

parser = argparse.ArgumentParser()
parser.add_argument('path', nargs='?', type=str, default=None)
args = parser.parse_args()

path: str = args.path


def sort_files(sorting: str, ftype, files: dict, duplicates: str = 'no', deletion: list = []) -> int:

    if sorting == '1':
        files: dict = dict(sorted(files.items(), reverse=True))
    elif sorting == '2':
        files: dict = dict(sorted(files.items()))

    dupes: int = 1
    freed: int = 0

    for byte, hashes in files.items():
        if not deletion:
            print(f"\n{byte} bytes")

        if duplicates == 'yes':
            for hash_code in hashes:
                if len(hashes[hash_code]) > 1:
                    if not hashes[hash_code][0].endswith(ftype):
                        continue

                    if not deletion:
                        print(f"Hash: {hash_code}")

                    for file in hashes[hash_code]:
                        if not deletion:
                            print(f"{dupes}. {file}")
                        else:
                            if dupes in deletion:
                                os.remove(file)
                                freed += byte

                        dupes += 1

        elif duplicates == 'no':
            for _, file in hashes.items():
                for ind in file:
                    if ind.endswith(ftype):
                        print(ind)

    if freed:
        print(f"\nTotal freed up space: {freed} bytes")

    return dupes - 1


def get_files(directory: str) -> Tuple[set, dict]:

    types: set = set()
    sizes: dict = {}

    if path:
        for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
            for name in filenames:
                fullpath: str = os.path.join(dirpath, name)
                size: int = os.path.getsize(fullpath)
                file_type: List[str] = name.split('.')
                types.add(file_type[-1])

                with open(fullpath, 'rb') as opened:
                    md5 = hashlib.md5()
                    content = opened.read()
                    md5.update(content)
                    hash_hex = md5.hexdigest()

                    if size not in sizes:
                        sizes[size]: dict = {hash_hex: [fullpath]}
                    elif hash_hex not in sizes[size]:
                        sizes[size][hash_hex]: List[str] = [fullpath]
                    else:
                        sizes[size][hash_hex].append(fullpath)
    else:
        print("Directory is not specified")
        sys.exit()

    for _, hashes in sizes.items():
        for hash_code, lists in hashes.items():
            lists.sort()

    types.add('')

    return types, sizes


file_types, info = get_files(path)

while True:

    file_format: str = input("Enter file format:\n")

    if file_format not in file_types:
        print("Wrong option")
        continue

    break

print("""
Size sorting options:
1. Descending
2. Ascending
""")

while True:

    option: str = input("Enter a sorting option:\n")

    if option not in ('1', '2'):
        print("Wrong option")
        continue

    break

sort_files(option, file_format, info)


while True:

    dups: str = input("\nCheck for duplicates?\n").lower()

    if dups not in ('yes', 'no'):
        print("Wrong option")
        continue

    break

if dups == 'yes':
    dup_count = sort_files(option, file_format, info, dups)

while True:

    delete: str = input("\nDelete files?\n").lower()

    if delete not in ('yes', 'no'):
        print("Wrong option")
        continue

    break

if delete == 'yes':
    while True:

        num_delete: List[str] = input("\nEnter file numbers to delete:\n").split()

        if num_delete:
            try:
                num_delete: List[int] = [int(x) for x in num_delete]
            except ValueError:
                print("Wrong format")
                continue
        else:
            print("Wrong format")
            continue

        if max(num_delete) > dup_count or min(num_delete) < 1:
            print("Wrong format")
            continue

        break

    sort_files(option, file_format, info, duplicates=dups, deletion=num_delete)
