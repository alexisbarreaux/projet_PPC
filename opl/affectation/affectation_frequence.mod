/*********************************************
 * OPL 22.1.0.0 Model
 * Author: alexi
 * Creation Date: 26 déc. 2022 at 14:42:23
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
   	// Constraint used for max frequency
    forall(transmitter in transmitters)
      transmitterFrequency[transmitter] <= nbFrequencies;     
}

// Printing results
main {
   currentModel= thisOplModel;
   currentModel.generate();
   cp.param.SearchType="DepthFirst";
   cp.param.Workers=1;
   cp.startNewSearch();
   var data = currentModel.dataElements;

   var  n = 0;
   var maxFreq= -1;
   var currentMax = 0;
   while (cp.solve() && n < 100) { 
     n++;
     currentMax = 0;
   	 write(n + "th solution. ");
   	 writeln(currentModel.transmitterFrequency);
   	 for (var transmitter in currentModel.transmitterFrequency){
       if(currentModel.transmitterFrequency[transmitter] > currentMax){
         currentMax = currentModel.transmitterFrequency[transmitter];
       }
  }    
  
     // Decrement max frequency
     if(maxFreq <0 || maxFreq >= currentMax){
       writeln("Max freq " + currentMax);
       maxFreq = currentMax - 1;
       data.nbFrequencies= maxFreq;
       var def = currentModel.modelDefinition;
	   currentModel = new IloOplModel(def,cp);
		currentModel.addDataSource(data);
		currentModel.generate();
     }
       writeln();
   }   
}