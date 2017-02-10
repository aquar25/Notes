#!/bin/bash

cd ./comics

for file in ./*
do 
    if test -d "$file"
    then
    	zip -rj "$file".zip "$file"
    	echo "$file"
    fi
done