# Versie 1:
# Model met 1 trein op spoor 0 en TVP announcement
# LPS = 27kb
# LTS = 88 states, 201 Transitions, time = 0.5 seconde
# Compiled rewriter geeft segmenatation fault
# Model zonder global variables
mcrl22lps -c -b -w --balance-summands -a --timings ../Crossing_spec.mcrl2 | lpssumelm -vc - crossing.lps;
lps2lts -v --save-at-end --cached --rewriter=jittyc --timings crossing.lps crossing.lts;