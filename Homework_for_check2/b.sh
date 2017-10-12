#!/bin/bash
read arg
for i in {1..30}
  do
    python othello.py $arg random1
  done
