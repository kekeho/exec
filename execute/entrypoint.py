#!/usr/bin/env python3
import sys
import os

if __name__ == "__main__":
    if len(sys.argv) == 1:
        # No script given
        raise ValueError('No script given')

    uuid = sys.argv[1]
    filename = os.path.join('scripts', uuid + '.py') 
    with open(filename, 'r') as file:
        script = file.read()
        exec(script)
