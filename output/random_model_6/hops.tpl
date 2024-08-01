//Number of population samples (demes)
5
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
N_POP3$
N_POPG$
//Sample Sizes
18
19
41
20
0
//Growth rates : negative growth implies population expansion
0
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
5
//Migration matrix 0
0.000 MIG01$ MIG02$ MIG03$ MIG0G$
MIG10$ 0.000 MIG12$ MIG13$ MIG1G$
MIG20$ MIG21$ 0.000 MIG23$ MIG2G$
MIG30$ MIG31$ MIG32$ 0.000 MIG3G$
MIGG0$ MIGG1$ MIGG2$ MIGG3$ 0.000
//Migration matrix 1
0.000 MIG01$ MIG02$ MIG03$ 0.000
MIG10$ 0.000 MIG12$ MIG13$ 0.000
MIG20$ MIG21$ 0.000 MIG23$ 0.000
MIG30$ MIG31$ MIG32$ 0.000 0.000
0.000 0.000 0.000 0.000 0.000
//Migration matrix 2
0.000 MIG01$ MIG02$ 0.000 0.000
MIG10$ 0.000 MIG12$ 0.000 0.000
MIG20$ MIG21$ 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
//Migration matrix 3
0.000 MIG01$ 0.000 0.000 0.000
MIG10$ 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
//Migration matrix 4
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
6 historical event
T_BOTGG$ 5 5 0 RESBOTGG$ 0 1
T_BOTENDGG$ 5 5 0 RESBOTENDGG$ 0 1
T_DIVG0$ 4 0 1 1 0 1
T_DIV31$ 3 1 1 1 0 2
T_DIV20$ 2 0 1 1 0 3
T_DIV01$ 0 1 1 1 0 4
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
