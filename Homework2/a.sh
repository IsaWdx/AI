#!/bin/bash
read arg
for i in {0..25}
  do
    python othello.py $arg random1
  done
