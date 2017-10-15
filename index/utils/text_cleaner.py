#!/usr/bin/env python

import utils.config_text_cleaner as conf
import re

class Cleaner:

    def __init__(self):
        self.token_utils = TokenStructure()

    def tokenize(self, text):
        return text.strip().split()

    def remove_noise(self, tokens):
        modified_tokens = []
        for token in tokens:
            #if token in stopwords continue to the next token
            if token in conf.noise:
                continue
            modified_tokens.append(token)        

        return modified_tokens

    def encode_initials(self, tokens):
        modified_tokens = []
        for token in tokens:
            if self.token_utils.is_name_abbreviation(token):
                token = token[:-1] + "_DOT"
            modified_tokens.append(token)
        return modified_tokens

    def decode_initials(self, tokens):
        modified_tokens = []
        for token in tokens:
            if token.endswith("_DOT"):
                token = token[:-4] + "."
            modified_tokens.append(token)
        return modified_tokens
    
    def clean_years(self, tokens):
        modified_tokens = []
        for token in tokens:
            if self.token_utils.is_a_year(token):
                if token.startswith((".", "-", "+", "*", ",")):
                    token = token[1:]
                if token.endswith((".", "-", "+", "*", ",")):
                    token = token[:-1]
            modified_tokens.append(token)
        return modified_tokens
            
    def remove_invalid_tokens(self, tokens):
        modified_tokens = []
        for token in tokens:
            if not self.token_utils.is_an_invalid_word(token):
               modified_tokens.append(token)
        return modified_tokens

    def strip_special_characters(self, tokens):
        modified_tokens = []
        for token in tokens:
            strip_at_first = True
            while strip_at_first:
                if len(token) > 0 and token[0] in conf.special_characters:
                    token = token[1:]
                else:
                    strip_at_first = False
                    
            strip_at_last = True
            while strip_at_last:
                if len(token) > 0 and token[-1] in conf.special_characters:
                    token = token[:-1]
                else:
                    strip_at_last = False

            if len(token) > 0:
                modified_tokens.append(token)
        return modified_tokens

    # split by =, -?, 
    def clean_text(self, text):
        if len(text) > 0:
            original_tokens = self.tokenize(text)
            cleaned_tokens = self.remove_noise(original_tokens)
            cleaned_tokens = self.encode_initials(cleaned_tokens)
            cleaned_tokens = self.clean_years(cleaned_tokens)
            cleaned_tokens = self.remove_invalid_tokens(cleaned_tokens)
            cleaned_tokens = self.strip_special_characters(cleaned_tokens)
            cleaned_tokens = self.remove_noise(cleaned_tokens)
            cleaned_tokens = self.decode_initials(cleaned_tokens)
            return " ".join(cleaned_tokens)

        return ""
    
    
class TokenStructure:

    def __init__(self):
       self.regex_year = re.compile('^[.\-+*,]?[0-9]+[.\-+*,]?$')
    
    def is_a_year(self, token):
        if re.match(self.regex_year, token):
            return True
        return False

    def is_name_abbreviation(self, token):
        if len(token) > 0 and len(token) <= 4 and token[0].isupper() and token[-1] == '.':
            return True
        return False
    
    def is_an_invalid_word(self, token):
        chars_count = len(token)
        special_chars_count = 0
        for char in token:
            if char.isdigit():
                special_chars_count += 1
            elif char in conf.special_characters:
                special_chars_count += 1

        special_chars_freq = (1.0*special_chars_count)/chars_count
        if chars_count >= 3 and special_chars_freq >= conf.special_chars_threshold:
            return True
        return False
