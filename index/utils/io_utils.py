#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

"""
I/O utility functions
"""

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.mkdir(directory_name)

def save_file(file_content, filename):
    print(filename)
    with open(filename, "w") as f:
        f.write(file_content)

def list_files_in_dir(directory):
    files = [f for f in os.listdir(directory) if f.endswith(".txt")]
    return files

def load_file_rows(filename):
    file_content = []
    with open(filename, "r") as f:
        for line in f:
            file_content.append(line)
    return file_content
