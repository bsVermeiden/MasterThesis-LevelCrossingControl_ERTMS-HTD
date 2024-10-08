lts2pbes --formula="../properties/Maximum_Warning_Time.mcf" -c crossing.lts | pbessolve --file=crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;