#!/usr/bin/env python

class Printer:
    
    def print_dict(self, dict_to_print):

        for key in dict_to_print.keys():
            print("---->")
            print("{0}:\n{1}".format(key, dict_to_print[key]))
            print("<-----\n")

    def print_token_frequency(self, frequencies):
        for counter, frequency in enumerate(frequencies):
            print("{0}, {1}, {2}".format(counter,
                                         str(frequency[0]),
                                         frequency[1]))
 
