lts2pbes --formula="../properties/If_train_on_LX_then_lx_active_for_at_least_ANNOUNCEMENT_TIME.mcf" -c ./crossing.lts | pbessolve --file=./crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;