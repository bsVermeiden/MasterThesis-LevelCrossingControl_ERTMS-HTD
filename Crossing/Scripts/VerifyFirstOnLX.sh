lts2pbes --formula="../properties/All_trains_are_on_lx_first_time.mcf" -c ./crossing.lts | pbessolve --file=./crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;