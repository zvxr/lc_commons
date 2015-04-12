#!/bin/bash

# Variables
DATABASE=${1:-"lc_commons.db"}
OUTPUT=${2:-"lc_commons_loans_over_time.csv"}

# Loans by ID over time.
sqlite3 $DATABASE <<!
.headers on
.mode csv
.output $OUTPUT
select * from loansFundedAsOfDate order by id, asOfDate;
!
