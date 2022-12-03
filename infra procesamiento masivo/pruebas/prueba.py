import sys

for line in sys.stdin:
    index, app, category, rating, reviews, installs, type_, price = line.strip("\n").split("\,")
    if type == "Paid" and rating > 4:
        print(f"{app},{category},{rating},{reviews},{installs},{price}")
    