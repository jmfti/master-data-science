#!/usr/bin/env python3
import sys, os, re
from mrjob.job import MRJob

class MRJoin(MRJob):
    countries = {}
    
    def mapper(self, _, line):
        splits = line.rstrip("\n").split(",")

        if len(splits) == 2: # datos de paises
            countryCode = splits[1]
            countryName = splits[0]
            self.countries[countryCode] = countryName
        else: #  datos de personas
            name = splits[0]
            vote = splits[1]
            countryCode = splits[2]
            yield countryCode, 1

    def reducer(self, key, values):
        if not key in self.countries:
            yield key, sum(values)
        else:
            yield self.countries[key], sum(values)

if __name__ == '__main__':
    MRJoin.run()
