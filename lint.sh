#!/bin/bash

python3 gen.py

if ! git diff-index --quiet HEAD --; then
  echo "The generated Dockerfiles don't match the template"
  echo "Please update them"
  git diff HEAD
  exit 1
fi
