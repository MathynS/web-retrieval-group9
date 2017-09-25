#!/usr/bin/env python

import io_utils as io
from text_cleaner import Cleaner
import config_text_cleaner as conf

def test_stopwords_removal():
    original_content = io.load_file_rows(conf.STOP_WORDS_TEST_INPUT_FILE)
    cleaned_content = ""
    cleaner = Cleaner()
    for row in original_content:
        print("row: {0}".format(row))
        cleaned_content += cleaner.clean_text(row) + "\n"
    io.save_file(cleaned_content, conf.STOP_WORDS_TEST_OUTPUT_FILE)

def test_special_characters_removal():
    original_content = io.load_file_rows(conf.SPECIAL_CHARACTERS_TEST_INPUT_FILE)
    cleaned_content = ""
    cleaner = Cleaner()
    for row in original_content:
        cleaned_content += cleaner.clean_text(row) + "\n"
    io.save_file(cleaned_content, conf.SPECIAL_CHARACTERS_TEST_OUTPUT_FILE)

if __name__ == '__main__':
    test_stopwords_removal()
    test_special_characters_removal()
