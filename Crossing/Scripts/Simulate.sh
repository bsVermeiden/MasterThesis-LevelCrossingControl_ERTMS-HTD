mcrl22lps -f -c -b -w --balance-summands -a ../Crossing_spec.mcrl2 crossing.lps;
lpssumelm -c crossing.lps crossing.lps;
lpsbinary crossing.lps crossing.lps;
lpssumelm -c crossing.lps crossing.lps;
lpsrewr -pcondition-one-point crossing.lps crossing.lps;
lpsinfo crossing.lps
lpsxsim crossing.lps