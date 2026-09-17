#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) >= 5:
        item = fields[3]
        price = fields[4]
        try:
            price = float(price)
            print("%s\t%s" % (item, price))
        except:
            pass
