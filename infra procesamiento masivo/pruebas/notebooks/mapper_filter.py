#!/usr/bin/env python3
import sys

for line in sys.stdin:
    index, app, category, rating, reviews, installs, type_, price = line.strip('\n').split(',')
    if type_ == "Paid":
        print(f"{app},{category},{rating},{reviews},{installs},{price}")
    
