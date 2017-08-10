// Python Serial Link
// 2.0
// 48 Vertical Syringe Pump
// Written by Taylor Howell
// July 2015

int directionPin = 8;
int stepPin = 9;
int LED = 13;
float DWtimedelay;
float Stimedelay;

void setup(){
  Serial.begin(9600);
  pinMode(directionPin,OUTPUT); // direction pin (again may want to put it somewhere else)
  pinMode(stepPin,OUTPUT); // step pin 
  pinMode(LED,OUTPUT);
  
//  // Digital Write Delay Calibration
//  float DWtimedelay = micros();
//  for(int i = 1; i <=10000; i++){
//    digitalWrite(13, HIGH);                
//    digitalWrite(13, LOW); 
//  }   
//  DWtimedelay = micros() - DWtimedelay;
//  //Serial.print("Time per digitalWrite: "); Serial.println(DWtimedelay/10000/2);
//  
//  // Serial Read Delay Calibration
//  float Stimedelay = micros();
//  char s;
//  for(int i = 1; i <=10000; i++){
//    s = Serial.read();
//  }   
//  Stimedelay = micros() - Stimedelay;
  powerdown();
}

void up(){
  //Serial.println("Up...");
  float currentSteps = 0;
  digitalWrite(directionPin, LOW);
  while(currentSteps < 2080){
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(50);
      currentSteps = currentSteps + 1;
  }
  //Serial.println("Up complete");
}

void down(){
  //Serial.println("Down...");
  float currentSteps = 0;
  digitalWrite(directionPin, HIGH);
  while(currentSteps <= 2080){
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(50);
      digitalWrite(stepPin,LOW);
      delayMicroseconds(50);
      currentSteps = currentSteps + 1;
  }
  Serial.println("Down complete");
}

void flow(float numberSteps, float timeStep){
  float currentSteps = 0;
  char s;
  boolean p = 1;
  boolean q = 1;
  digitalWrite(directionPin, HIGH);
  Serial.flush();
  
  if (timeStep < 1000){
     timeStep = timeStep - 20; //digitalWrite delay and Serial.read()
     while(currentSteps <= numberSteps){
       if(Serial.available() == 1){
       s = Serial.read();
       
        if (s == 'p'){
          while(p == 1){
            while( Serial.available() == 0){}
            s = Serial.read();
            if (s == 'u'){
              p = 0;
            }
            if (s == 's'){
              p = 0;
              q = 0;
            }
          }
          
        }
        if (q == 0){
          break;
        }
        p = 1;
        q = 1;
       }
        
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(timeStep);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(timeStep);
        currentSteps = currentSteps + 1;
    }
  }
  
  else if (timeStep >= 1000){
     timeStep = timeStep - 20; //digitalWrite delay and Serial.read()
     timeStep = timeStep/1000; //convert to ms from microseconds
     while(currentSteps <= numberSteps){
       if(Serial.available() == 1){
       s = Serial.read();
       
        if (s == 'p'){
          while(p == 1){
            while( Serial.available() == 0){}
            s = Serial.read();
            if (s == 'u'){
              p = 0;
            }
            if (s == 's'){
              p = 0;
              q = 0;
            }
          }
          
        }
        if (q == 0){
          break;
        }
        p = 1;
        q = 1;
       }
        
        digitalWrite(stepPin,HIGH);
        delay(timeStep);
        digitalWrite(stepPin,LOW);
        delay(timeStep);
        currentSteps = currentSteps + 1;
    } 
  }
}

void withdraw(float numberSteps, float timeStep){
  float currentSteps = 0;
  char s;
  boolean p = 1;
  boolean q = 1;
  digitalWrite(directionPin,LOW);
  Serial.flush();
  
  if (timeStep < 1000){
     timeStep = timeStep - 20; //digitalWrite delay and Serial.read()
     while(currentSteps <= numberSteps){
       if(Serial.available() == 1){
       s = Serial.read();
       
        if (s == 'p'){
          while(p == 1){
            while( Serial.available() == 0){}
            s = Serial.read();
            if (s == 'u'){
              p = 0;
            }
            if (s == 's'){
              p = 0;
              q = 0;
            }
          }
          
        }
        if (q == 0){
          break;
        }
        p = 1;
        q = 1;
       }
        
        digitalWrite(stepPin,HIGH);
        delayMicroseconds(timeStep);
        digitalWrite(stepPin,LOW);
        delayMicroseconds(timeStep);
        currentSteps = currentSteps + 1;
    }
  }
  
  else if (timeStep >= 1000){
     timeStep = timeStep - 20; //digitalWrite delay and Serial.read()
     timeStep = timeStep/1000; //convert to ms from microseconds
     while(currentSteps <= numberSteps){
       if(Serial.available() == 1){
       s = Serial.read();
       
        if (s == 'p'){
          while(p == 1){
            while( Serial.available() == 0){}
            s = Serial.read();
            if (s == 'u'){
              p = 0;
            }
            if (s == 's'){
              p = 0;
              q = 0;
            }
          }
          
        }
        if (q == 0){
          break;
        }
        p = 1;
        q = 1;
       }
        
        digitalWrite(stepPin,HIGH);
        delay(timeStep);
        digitalWrite(stepPin,LOW);
        delay(timeStep);
        currentSteps = currentSteps + 1;
    } 
  } 
}

void powerdown(){
  digitalWrite(stepPin,LOW);
  digitalWrite(directionPin,LOW);
}

void loop(){
  powerdown();
  
  String command = "";
  if (Serial.available() >6) {
    delay(50);
    while(Serial.available() > 0){
      char c = Serial.read();  
      command += c; 
    }
  }
  
  if (command.length() >6) {
      Serial.flush();
      //Serial.println(command); 
      int i = 0;
      String func;
      String steps;
      String times;
        
      while (command[i] != ','){
        func += command[i];
        i = i + 1;
      }
      
      i = i + 1;
      
      while (command[i] != ','){
        steps += (char)command[i];
        i = i + 1;
      }
      
      i = i + 1;
      
      while (command[i] != ','){
        times += (char)command[i];
        i = i + 1;
      }
      

    if (func == "up"){
      up();
    }
      
    if (func == "down"){
      down();
    } 
    
    if (func == "flow" ){
      float a = steps.toFloat();
      float b = times.toFloat();
      flow(a,b);
      powerdown();
    }  
    
    if (func == "with"){
      float a = steps.toFloat();
      float b = times.toFloat();
      withdraw(a,b);
      powerdown();
    }
  }
} 
  
