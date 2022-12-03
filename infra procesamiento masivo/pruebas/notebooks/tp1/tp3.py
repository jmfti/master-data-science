#!/usr/bin/env python3
import sys, os, re
from mrjob.job import MRJob
from mrjob.step import MRStep

class MRJoin(MRJob):
    countries = {}
    
    def mapper_countries_goods(self, _, line):
        splits = line.rstrip("\n").split(",")
        #si es un pais nos lo guardamos para posterior consulta, sino emitimos un <pais>,1 para que el combiner sume
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
        # suma de los buenos por paises, esto se le pasa a reducer_count_goods
        yield (country, sum(counts))
    
    def reducer_count_goods(self, country, counts):
        # manda todos los (suma(buenos), pais) al mismo reducer
        yield None, (sum(counts), country)
    
    
    def reducer_find_max_goods(self, _, goods_count_pairs):
        # el reducer final recibe (None, serializado(counts, country))
        items = list(goods_count_pairs)
        max_item = max(items)
        filtered_items = filter(lambda item: item[0] == max_item[0], items)
        for item in filtered_items:
            yield item[0], self.countries[item[1]]
        
    
    def steps(self):
        return [
            MRStep(mapper=self.mapper_countries_goods,
                   combiner=self.combiner_count_goods,
                   reducer=self.reducer_count_goods),
            MRStep(reducer=self.reducer_find_max_goods)
        ]
        

if __name__ == '__main__':
    MRJoin.run()
