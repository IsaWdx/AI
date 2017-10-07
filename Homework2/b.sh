#!/bin/bash
read arg
for i in {0..30}
  do
    python othello.py $arg random1
  done
