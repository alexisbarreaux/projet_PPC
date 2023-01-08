/*********************************************
 * OPL 22.1.0.0 Model
 * Author: sulia
 * Creation Date: 7 janv. 2023 at 17:00:22
 *********************************************/
using CP;
   
 
 // Definition des données du problèmes
int dimension = ...;

range centre = 3..dimension+2;
range large = 1..dimension+4;
 
 // Variables de décision
 
dvar int cavaliers[i in large, j in large] in 0..1;

minimize sum(i in centre, j in centre) cavaliers[i][j];

 // Contraintes
 constraints {
   
  	// Une case n'est couverte que si un cavalier la couvre
  	forall (i in centre) {
    	forall (j in centre) {
    	   1 <= cavaliers[i][j] + cavaliers[i-1][j-2] + cavaliers[i+1][j-2] + cavaliers[i-1][j+2] + cavaliers[i+1][j+2] + cavaliers[i-2][j-1] + cavaliers[i-2][j+1] + cavaliers[i+2][j-1] + cavaliers[i+2][j+1];    
	  	}  
  	}
  	
  	// Les cavaliers ne peuvent pas être placés sur le bord artificiel de l'échiquier
  	forall (i in large) {
    	forall (j in 1..2) {
    	   cavaliers[i][j] == 0;    
	  	}  
  	}
  	
  	forall (i in large) {
    	forall (j in dimension+3..dimension+4) {
    	   cavaliers[i][j] == 0;    
	  	}  
  	}
  	
  	forall (i in 1..2) {
    	forall (j in large) {
    	   cavaliers[i][j] == 0;    
	  	}  
  	}
  	
  	forall (i in dimension+3..dimension+4) {
    	forall (j in large) {
    	   cavaliers[i][j] == 0;    
	  	}  
  	}

};

main {
	var f = cp.factory;
	var phase1 = f.searchPhase( thisOplModel.cavaliers,
		f.selectSmallest(f.domainSize()), 
		f.selectSmallest(f.value()));
	
	var phase2 = f.searchPhase( thisOplModel.cavaliers,
		f.selectLargest(f.domainSize()), 
		f.selectSmallest(f.value()));
		
	var phase3 = f.searchPhase( thisOplModel.cavaliers,
		f.selectSmallest(f.varIndex(thisOplModel.cavaliers)), 
		f.selectSmallest(f.value()));
		
	var phase4 = f.searchPhase( thisOplModel.cavaliers,
		f.selectLargest(f.varIndex(thisOplModel.cavaliers)), 
		f.selectSmallest(f.value()));
	
	var phase5 = f.searchPhase( thisOplModel.cavaliers,
		f.selectSmallest(f.varIndex(thisOplModel.cavaliers)), 
		f.selectRandomValue());
	
	cp.setSearchPhases(phase5); 
	thisOplModel.generate();
	cp.solve();
}