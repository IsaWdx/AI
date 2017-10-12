#!/bin/bash
read arg1
read arg2
for i in {1..5}
  do
    python othello.py $arg1 $arg2
    python othello.py  $arg2 $arg1
  done
