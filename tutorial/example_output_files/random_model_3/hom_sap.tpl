//Number of population samples (demes)
4
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
N_POPG$
//Sample Sizes
15
15
15
0
//Growth rates : negative growth implies population expansion
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
4
//Migration matrix 0
0.000 MIG01$ MIG02$ MIG0G$
MIG10$ 0.000 MIG12$ MIG1G$
MIG20$ MIG21$ 0.000 MIG2G$
MIGG0$ MIGG1$ MIGG2$ 0.000
//Migration matrix 1
0.000 MIG01$ 0.000 MIG0G$
MIG10$ 0.000 0.000 MIG1G$
0.000 0.000 0.000 0.000
MIGG0$ MIGG1$ 0.000 0.000
//Migration matrix 2
0.000 0.000 0.000 MIG0G$
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
MIGG0$ 0.000 0.000 0.000
//Migration matrix 3
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
4 historical event
T_ADMIX20$ 2 0 0.535511181168016 1 0 0
T_DIV20$ 2 0 1 1 0 1
T_DIV10$ 1 0 1 1 0 2
T_DIV0G$ 0 3 1 1 0 3
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
