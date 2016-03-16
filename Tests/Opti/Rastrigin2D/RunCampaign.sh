#!/bin/bash

DUH=../../..

ntrials=$1

for i in `seq -w $ntrials`; do
	$DUH/Launcher ./OptiGA.case
	mv Rastrigin2D.history.dat Rastrigin2D.history.$i.dat
done

rm Rastrigin2D.history.all.dat
awk 'FNR == 1 { print ""; print ""; print "" } { print }' Rastrigin2D.history.[0-9]*.dat > Rastrigin2D.history.all.dat

