#!/bin/bash

#Launches 3 series (-E3) of 2 simulations (-n2) of genetic diversity in 2 populations 
#having an ancesral botnleneck and a population resize
#We generate a genotype table (-G) of the resulting diversity, where genotypes are from diploid individuals (-g)

#The parameters are drawn from priors defined in the est file, and the search ranges 
#of two of them directly depend on other parameters 

./fsc  -t 2PopDNABotRand.tpl -e 2PopDNABotRand.est -n2 -E3 -G -g 