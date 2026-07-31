float lineal = 0.0;
float angular = 0.0;

void setup() {
  Serial.begin(115200);
  // aqui configuras los pines de tu puente H (ej. pinMode(pin_in1, OUTPUT);)
}

void loop() {
  if (Serial.available() > 0) {
    String comando = Serial.readStringUntil('\n');
    
    // separamos la velocidad lineal y angular
    int coma = comando.indexOf(',');
    if (coma > 0) {
      lineal = comando.substring(0, coma).toFloat();
      angular = comando.substring(coma + 1).toFloat();
      
      // aqui llamas a tu funcion para mover los motores
      // mover_motores(lineal, angular);
    }
  }
}