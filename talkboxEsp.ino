// === Basic ESP32 Voice Assistant Display Framework ===
// 🧠 Serial animation receiver + display hook-up

// === Animation State ===
String currentAnimation = "";
unsigned long animationStartTime = 0;

// === Setup ===
void setup() {
  Serial.begin(115200);
  // initializeDisplay();         // TODO: Init GC9A01 screen
  // initializeSpeaker();         // TODO: Init speaker if needed
  // initializeMic();             // TODO: Init mic if needed
  // showBootScreen();            // Optional splash screen
  Serial.println("🎯 ESP32 Ready for animation commands.");
}

// === Main Loop ===
void loop() {
  // === Read Serial Input ===
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();

    if (input.startsWith("ANIM:")) {
      String anim = input.substring(5);
      runAnimation(anim);
    }
  }

  // === Optional: Handle repeating animation frames here ===
  updateAnimation();
}

// === Run Animation by Name ===
void runAnimation(String name) {
  currentAnimation = name;
  animationStartTime = millis();

  Serial.print("🎭 Running animation: ");
  Serial.println(name);

  if (name == "talk") {
    playTalkFrame();
  } else if (name == "blink") {
    playBlinkFrame();
  } else if (name == "smile") {
    playSmileFrame();
  } else if (name == "look") {
    playLookFrame();
  } else if (name == "open mouth") {
    drawOpenMouth();
  } else if (name == "close mouth") {
    drawClosedMouth();
  } else if (name == "neutral") {
    drawNeutralFace();
  } else {
    Serial.println("❌ Unknown animation.");
  }
}

// === Frame Functions (Stubbed for now) ===
void playTalkFrame() {
  // TODO: Draw a frame of talking
  Serial.println("[FRAME] Talking...");
}

void playBlinkFrame() {
  // TODO: Close and reopen eyes
  Serial.println("[FRAME] Blink.");
}

void playSmileFrame() {
  // TODO: Show smiling mouth
  Serial.println("[FRAME] Smile.");
}

void playLookFrame() {
  // TODO: Move eyes in a direction
  Serial.println("[FRAME] Look left/right.");
}

void drawOpenMouth() {
  // TODO: Open mouth visual
  Serial.println("[FRAME] Open mouth.");
}

void drawClosedMouth() {
  // TODO: Closed mouth visual
  Serial.println("[FRAME] Close mouth.");
}

void drawNeutralFace() {
  // TODO: Neutral resting face
  Serial.println("[FRAME] Neutral face.");
}

// === Animation Handler (for timing-based updates) ===
void updateAnimation() {
  // Example: If blink is supposed to last 300ms
  if (currentAnimation == "blink" && millis() - animationStartTime > 300) {
    drawNeutralFace();  // Go back to neutral
    currentAnimation = "";
  }
}
