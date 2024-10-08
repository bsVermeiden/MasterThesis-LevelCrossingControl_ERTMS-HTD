lts2pbes --formula="../properties/If_no_train_close_to_the_LX_then_the_LX_must_be_deactivated.mcf" -c ./crossing.lts | pbessolve --file=./crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;