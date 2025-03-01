#include <Arduino.h>

const int num_sliders = 1;
int slider_pins[num_sliders] = {A0};

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