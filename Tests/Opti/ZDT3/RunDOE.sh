#!/bin/bash

DUH=../../../
DOEGENERATOR=$DUH/DOEGenerator
LAUNCHER=$DUH/Launcher

rm -f DOE0.plan
$DOEGENERATOR ./ZDT3.chain LHS 10 DOE0.plan

$LAUNCHER ./DOE.case

mv DOE_out.plan DOE.plan
