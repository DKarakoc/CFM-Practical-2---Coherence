#!/bin/bash

counter=1
until [ $counter -gt 10 ] # change this number for how many times you want to run it
do
	./D_Coh.py >> D_Coh_Results.txt
	((counter++))
done

./diagrams.py

