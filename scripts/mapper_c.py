#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) >= 5:
        store = fields[2]
        price = fields[4]
        try:
            price = float(price)
            print("%s\t%s" % (store, price))
        except:
            pass
