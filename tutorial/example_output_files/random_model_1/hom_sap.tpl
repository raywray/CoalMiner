//Number of population samples (demes)
3
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
//Sample Sizes
15
15
15
//Growth rates : negative growth implies population expansion
0
0
0
//Number of migration matrices : 0 implies no migration between demes
3
//Migration matrix 0
0.000 MIG01$ MIG02$
MIG10$ 0.000 MIG12$
MIG20$ MIG21$ 0.000
//Migration matrix 1
0.000 0.000 MIG02$
0.000 0.000 0.000
MIG20$ 0.000 0.000
//Migration matrix 2
0.000 0.000 0.000
0.000 0.000 0.000
0.000 0.000 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
3 historical event
T_ADMIX12$ 1 2 0.4032201595483088 1 0 1
T_DIV12$ 1 2 1 1 0 1
T_DIV20$ 2 0 1 RELANC20$ 0 2
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
