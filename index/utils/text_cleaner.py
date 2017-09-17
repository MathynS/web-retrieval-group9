#!/usr/bin/env python


class Cleaner:
    def tokenize(self, text):
        return text.strip().split()

    
    def clean_text(self, text):
        return self.tokenize(text)
