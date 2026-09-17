#!/usr/bin/env python
import sys

current_store = None
total = 0.0
count = 0

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    store = parts[0]
    price = float(parts[1])
    if current_store == store:
        total += price
        count += 1
    else:
        if current_store is not None:
            print("%s\t%.2f" % (current_store, total / count))
        current_store = store
        total = price
        count = 1

if current_store is not None:
    print("%s\t%.2f" % (current_store, total / count))
