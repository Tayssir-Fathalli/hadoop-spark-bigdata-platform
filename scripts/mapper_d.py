#!/usr/bin/env python
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split('\t')
    if len(fields) >= 5:
        store = fields[2]
        item = fields[3]
        print("%s\t%s" % (store, item))
