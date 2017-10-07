#!/bin/bash
read arg
for i in {0..30}
  do
    python othello.py -aB -t 3000 $arg random1
  done
