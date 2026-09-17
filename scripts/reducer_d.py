#!/usr/bin/env python
import sys

current_store = None
item_counts = {}

for line in sys.stdin:
    line = line.strip()
    parts = line.split('\t')
    if len(parts) != 2:
        continue
    store = parts[0]
    item = parts[1]
    if current_store == store:
        item_counts[item] = item_counts.get(item, 0) + 1
    else:
        if current_store is not None:
            best_item = max(item_counts, key=item_counts.get)
            print("%s\t%s\t%d" % (current_store, best_item, item_counts[best_item]))
        current_store = store
        item_counts = {item: 1}

if current_store is not None:
    best_item = max(item_counts, key=item_counts.get)
    print("%s\t%s\t%d" % (current_store, best_item, item_counts[best_item]))
