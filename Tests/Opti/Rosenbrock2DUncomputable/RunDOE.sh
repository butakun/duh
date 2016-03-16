#!/bin/bash

DUH=../../../
DOEGENERATOR=$DUH/DOEGenerator
LAUNCHER=$DUH/Launcher

rm -f DOE0.plan
$DOEGENERATOR ./Rosenbrock2DUncomputable.chain LHS 6 DOE0.plan

$LAUNCHER ./DOE.case

