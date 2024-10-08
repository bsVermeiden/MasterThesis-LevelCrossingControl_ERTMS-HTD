lts2pbes --formula="../properties/All_trains_reach_the_end_of_their_track.mcf" -c crossing.lts | pbessolve --file=crossing.lts;
lts2lps .evidence.lts evidence.lps; 
lpsxsim evidence.lps;