#!/bin/bash

DUH=../../../
DOEGENERATOR=$DUH/DOEGenerator
LAUNCHER=$DUH/Launcher

if ! [ -f DOE.plan ]; then
	echo "You must run a DoE first, and rename DOE_out.plan to DOE.plan."
	exit 1
fi

$LAUNCHER ./OptiSurrogateGA.case

