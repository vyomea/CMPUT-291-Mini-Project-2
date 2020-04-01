#!/bin/bash

sort reviews.txt -u | perl break.pl | db_load -T -t hash rw.idx
sort pterms.txt -u | perl break.pl | db_load -c duplicates=1 -T -t btree pt.idx
sort rterms.txt -u | perl break.pl | db_load -c duplicates=1 -T -t btree rt.idx
sort scores.txt -u | perl break.pl | db_load -c duplicates=1 -T -t btree sc.idx
