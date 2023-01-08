/*********************************************
 * OPL 22.1.0.0 Model
 * Author: sulia
 * Creation Date: 6 janv. 2023 at 10:52:48
 *********************************************/
using CP;
   
 
 // Definition des donn�es du probl�mes
int dimension = ...;

range centre = 3..dimension+2;
range large = 1..dimension+4;
 
 // Variables de d�cision
 
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
  	
  	// Les cavaliers ne peuvent pas �tre plac�s sur le bord artificiel de l'�chiquier
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
  	
  	// Borne th�orique du probl�me
  	sum(i in centre, j in centre) cavaliers[i][j] >= 12;

};