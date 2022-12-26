/*********************************************
 * OPL 22.1.0.0 Model
 * Author: alexi
 * Creation Date: 26 déc. 2022 at 13:31:50
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
main {
   thisOplModel.generate();
   cp.startNewSearch();
   var  n = 1;
   while (cp.next() && n <= 10) { 
   	 write(n + "th solution. ");
   	 for (var transmitter in thisOplModel.transmitterFrequency)
                       write(thisOplModel.transmitterFrequency[transmitter]+  ",");
     n++;
     writeln()
    // master.oplModel.postProcess();
   }   
}
 