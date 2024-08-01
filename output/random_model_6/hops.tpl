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
0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
5 historical event
T_ADMIX0G$ 0 5 0.41712551292703404 1 0 0
T_DIV32$ 3 2 1 RELANC32$ 0 0
T_DIV10$ 1 0 1 RELANC10$ 0 0
T_DIV2G$ 2 4 1 RELANC2G$ 0 0
T_DIVG0$ 4 0 1 1 0 0
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
