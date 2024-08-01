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
0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
5 historical event
T_DIV13$ 1 3 1 1 0 0
T_BOT33$ 3 3 0 RESBOT33$ 0 0
T_BOTEND33$ 3 3 0 RESBOTEND33$ 0 0
T_DIV03$ 0 3 1 RELANC03$ 0 0
T_DIV23$ 2 3 1 RELANC23$ 0 0
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
