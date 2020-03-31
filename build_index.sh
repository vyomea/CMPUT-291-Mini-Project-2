#!/bin/bash

sort review.txt -u | perl break.pl | db_load -c -T -t hash rw.idx
sort pterms.txt -u | perl break.pl | db_load -c -T -t btree pt.idx
sort rterms.txt -u | perl break.pl | db_load -c -T -t btree rt.idx
sort scores.txt -u | perl break.pl | db_load -c -T -t btree sc.idx
