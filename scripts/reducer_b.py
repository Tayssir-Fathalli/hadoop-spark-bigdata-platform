#!/usr/bin/env python
import sys

current_item = None
total = 0.0
best_item = None
best_total = 0.0

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    item = parts[0]
    price = float(parts[1])
    if current_item == item:
        total += price
    else:
        if current_item is not None:
            if total > best_total:
                best_total = total
                best_item = current_item
        current_item = item
        total = price

if current_item is not None:
    if total > best_total:
        best_total = total
        best_item = current_item

print("%s\t%.2f" % (best_item, best_total))
