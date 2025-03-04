#include <Arduino.h>

const int num_sliders = 4;
int slider_pins[num_sliders] = {A0, A1, A2, A3};

// put function declarations here:

void setup() {
  Serial.begin(9600);
}

void loop() {
  for(int i = 0; i < num_sliders; i++){
    Serial.print(analogRead(slider_pins[i]));
    if (i < num_sliders - 1){
      Serial.print("|");
    }
  }
  Serial.print("\n");
  delay(10);
}