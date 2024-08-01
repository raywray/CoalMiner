//Number of population samples (demes)
2
//Population effective sizes (number of genes)
NPOP1
NPOP2
//Sample sizes
10
10
//Growth rates	: negative growth implies population expansion
0
0
//Number of migration matrices : 0 implies no migration between demes
0
//historical event: time, source, sink, migrants, new size, new growth rate, migr. matrix 
3  historical event
TDIV 0 1 1 1 0 0
TBOT 0 0 0 INTENSITY 0 0 instbot
TRESIZE 0 0 0 ANCSIZE 0 0 absoluteResize
//Number of independent loci [chromosome] 
1 0
//Per chromosome: Number of linkage blocks
1
//per Block: data type, num loci, rec. rate and mut rate + optional parameters
DNA 10000 0.00000 MUTRATE 0.33

