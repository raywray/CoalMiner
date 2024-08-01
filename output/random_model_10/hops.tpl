//Number of population samples (demes)
4
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
N_POP3$
//Sample Sizes
18
19
41
20
//Growth rates : negative growth implies population expansion
0
0
0
0
//Number of migration matrices : 0 implies no migration between demes
4
//Migration matrix 0
0.000 MIG01$ MIG02$ MIG03$
MIG10$ 0.000 MIG12$ MIG13$
MIG20$ MIG21$ 0.000 MIG23$
MIG30$ MIG31$ MIG32$ 0.000
//Migration matrix 1
0.000 MIG01$ MIG02$ 0.000
MIG10$ 0.000 MIG12$ 0.000
MIG20$ MIG21$ 0.000 0.000
0.000 0.000 0.000 0.000
//Migration matrix 2
0.000 0.000 MIG02$ 0.000
0.000 0.000 0.000 0.000
MIG20$ 0.000 0.000 0.000
0.000 0.000 0.000 0.000
//Migration matrix 3
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
0.000 0.000 0.000 0.000
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
4 historical event
T_ADMIX12$ 1 2 0.27502005816150243 1 0 1
T_DIV32$ 3 2 1 RELANC32$ 0 1
T_DIV10$ 1 0 1 1 0 2
T_DIV20$ 2 0 1 RELANC20$ 0 3
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
