#!/usr/bin/env python

class Printer:
    
    def print_dict(self, dict_to_print):

        for key in dict_to_print.keys():
            print("---->")
            print("{0}:\n{1}".format(key, dict_to_print[key]))
            print("<-----\n")

        
