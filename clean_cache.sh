#! /bin/sh 

find . -name "*.pyc" | grep -v "env"|xargs rm