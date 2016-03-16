#!/bin/bash

DUH=../../../
DOEGENERATOR=$DUH/DOEGenerator
LAUNCHER=$DUH/Launcher

rm -f DOE0.plan
$DOEGENERATOR ./Test.chain LHS 10 DOE0.plan

$LAUNCHER ./DOE.case

