//Number of population samples (demes)
4
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
N_POPG$
//Sample Sizes
30
30
30
0
//Growth rates : negative growth implies population expansion
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
2
//Migration matrix 0
0.000 MIG01$ MIG02$ MIG0G$
MIG10$ 0.000 MIG12$ MIG1G$
MIG20$ MIG21$ 0.000 MIG2G$
MIGG0$ MIGG1$ MIGG2$ 0.000
//Migration matrix 1
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
6 historical event
T_BOTGG$ 3 3 0 RESBOTGG$ 0 0
T_BOTENDGG$ 3 3 0 RESBOTENDGG$ 0 0
T_CONTACT$ -1 -1 0 1 0 1
T_DIVG2$ 3 2 1 1 0 1
T_DIV12$ 1 2 1 1 0 1
T_DIV02$ 0 2 1 1 0 1
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
