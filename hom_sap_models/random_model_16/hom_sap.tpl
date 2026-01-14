//Number of population samples (demes)
3
//Population effective sizes (number of genes)
N_POP0$
N_POP1$
N_POP2$
//Sample Sizes
30
30
30
//Growth rates : negative growth implies population expansion
0
0
0
//Number of migration matrices : 0 implies no migration between demes
0
//historical event: time, source, sink, migrants, new deme size, growth rate, migr mat index
5 historical event
T_DIV12$ 1 2 1 1 0 0
T_ADMIX02$ 0 2 0.9543775871146936 1 0 0
T_DIV02$ 0 2 1 1 0 0
T_BOT22$ 2 2 0 RESBOT22$ 0 0
T_BOTEND22$ 2 2 0 RESBOTEND22$ 0 0
//Number of independent loci [chromosome]
1 0
//Per chromosome: Number of contiguous linkage Block: a block is a set of contiguous loci
1
//per Block:data type, number of loci, per gen recomb and mut rates
FREQ 1 0 MUTRATE$ OUTEXP
