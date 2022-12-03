#!/usr/bin/env python3
import sys, os, re
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRJoin(MRJob):
    countries = {}
    
    def mapper_countries_goods(self, _, line):
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

    def combiner_count_goods(self, country, counts):
        # sum the words we've seen so far
        yield (country, sum(counts))

    def reducer_count_goods(self, country, counts):
        # send all (num_occurrences, word) pairs to the same reducer.
        yield None, (sum(counts), country)

    
    def reducer_find_max_goods(self, country, goods_count_pairs):
        # each item is (goods, country),
        # so yielding one results in key=counts, value=country
        max_item = max(goods_count_pairs)
        counts, country = max_item
        if country in self.countries:
            yield counts, self.countries[country]
        else:
            yield counts, country
        

    def steps(self):
        return [
            MRStep(mapper=self.mapper_countries_goods,
                   combiner=self.combiner_count_goods,
                   reducer=self.reducer_count_goods),
            MRStep(reducer=self.reducer_find_max_goods)
        ]
        

if __name__ == '__main__':
    MRJoin.run()
