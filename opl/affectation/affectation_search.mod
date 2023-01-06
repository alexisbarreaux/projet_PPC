/*********************************************
 * OPL 22.1.0.0 Model
 * Author: alexi
 * Creation Date: 26 déc. 2022 at 11:52:05
 *********************************************/

 using CP;
 
 // Data
int nbFrequencies = ...;
int nbTransmitters = ...;

range frequencies = 1..nbFrequencies;
range transmitters = 1..nbTransmitters;

tuple Offset {
  int firstTransmitter;
  int secondTransmitter;
  int value;
};

{Offset} offsets=...;
 
 // Decision variable, each variable stating what value is the frequency of the 
 // associated transmitter
 dvar int transmitterFrequency[transmitters] in frequencies;

minimize max(transmitter in transmitters) transmitterFrequency[transmitter];

 // Constraints
constraints {
    // Parity constraint
    forall(transmitter in transmitters)
      (transmitterFrequency[transmitter] + transmitter) mod 2 == 0;   
    forall(offset in offsets)
      abs(transmitterFrequency[offset.firstTransmitter] - transmitterFrequency[offset.secondTransmitter] ) 
      >= offset.value;      
}

// Printing results
main
 {
    var f = cp.factory;
    var smallest_domain_var_random_value = f.searchPhase(thisOplModel.transmitterFrequency,f.selectSmallest(f.domainSize()),  f.selectRandomValue());
    var smallest_var_random = f.searchPhase(thisOplModel.transmitterFrequency,f.selectSmallest(f.varIndex(thisOplModel.transmitterFrequency)),  f.selectRandomValue());
    var smallest_var= f.searchPhase(thisOplModel.transmitterFrequency,f.selectSmallest(f.varIndex(thisOplModel.transmitterFrequency)),  f.selectSmallest(f.value()));
    var small_var_smallest_value= f.searchPhase(thisOplModel.transmitterFrequency, f.selectSmallest(f.domainSize()),  f.selectSmallest(f.value()));
    cp.setSearchPhases(smallest_domain_var_random_value); 
 
   thisOplModel.generate();
   var n=0;
   var nMax = 10;
   cp.param.SearchType="DepthFirst";
   //cp.param.Workers=1;
   cp.solve()
  thisOplModel.postProcess();
 } 

 execute {
  write ("Results : ");
  writeln(thisOplModel.transmitterFrequency);

 	writeln("Offsets")  
  for(var offset in offsets){
    writeln(offset.firstTransmitter + " " + offset.secondTransmitter + " " + 
    Math.abs(transmitterFrequency[offset.firstTransmitter] - transmitterFrequency[offset.secondTransmitter]));
  }
}
 