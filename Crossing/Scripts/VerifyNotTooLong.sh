lts2pbes --formula="../properties/LX_warning_time_should_not_exceed_EXCEEDING_ANNOUNCEMENT_TIME.mcf" -c ./crossing.lts | pbessolve --file=./crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;