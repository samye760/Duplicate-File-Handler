# Duplicate-File-Handler

![Cryptographic hash algorithm](https://upload.wikimedia.org/wikipedia/commons/2/2b/Cryptographic_Hash_Function.svg)

This application uses the [os](https://docs.python.org/3/library/os.html) and [sys](https://docs.python.org/3/library/sys.html) Python built-in modules to parse user input using [argparse](https://docs.python.org/3/library/argparse.html) to find and delete duplicates files. 

## Features

The input directory will be parsed using [os.walk](https://www.tutorialspoint.com/python/os_walk.htm) to determine every file in ever subdirectory, which will then be printed out to the user. The user can then decide whether or not to print the duplicate files.

### Methodology

Duplicate files are determined using [hash functions](https://en.wikipedia.org/wiki/Hash_function) from the Python [hashlib](https://docs.python.org/3/library/hashlib.html) module using the [MD5 algorithm](https://en.wikipedia.org/wiki/MD5). Once the duplicates are determined, the user then chooses which files to delete from their file system which is then handled using os.remove.
