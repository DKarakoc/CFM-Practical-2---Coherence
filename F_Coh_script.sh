#!/bin/bash

counter=1
until [ $counter -gt 10 ] # change this number for how many times you want to run it
do
	echo "RUN NO: " $counter >> F_Coh_Results.txt
	./F_Coh.py >> F_Coh_Results.txt
	((counter++))
done

