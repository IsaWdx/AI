#!/bin/bash
read arg
read arg2
for i in {1..10}
  do
    python othello.py -aB -t 3000 $arg $arg2
  done
