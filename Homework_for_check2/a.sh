#!/bin/bash
read arg
for i in {1..30}
  do
    python othello.py -aB -t 30 $arg random1
  done
