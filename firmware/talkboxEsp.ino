/*
 * Gobber Voice Assistant - ESP32 Firmware
 * 
 * This firmware manages a state machine for the ESP32 to switch between two modes:
 * 1. LISTENING: Captures audio from an I2S microphone and streams it to a client (Python script).
 * 2. PLAYING_AUDIO: Receives a WAV file from the client and plays it on an I2S speaker.
 *
 * The Python script controls the state by sending a "PLAY" command over TCP, and the end
 * of playback is signaled by the client closing the connection.
 * 
 * Hardware Pins:
 *  - I2S Microphone: MCLK(not used), L/R CLK(15), BCLK(14), DIN(13)
 *  - I2S Speaker/DAC: BCLK(17), L/R CLK(18), DOUT(19)
 */

#include <WiFi.h>
#include <driver/i2s.h>

// === Wi-Fi Configuration ===
const char* ssid = "NETGEAR"; // <-- Your WiFi SSID
const char* password = "wideplanet973"; // <-- Your WiFi Password
const uint16_t TCP_PORT = 12345;

// === I2S Pin Configuration ===
// Microphone (RX)
#define I2S_MIC_BCLK      14
#define I2S_MIC_LRC       15
#define I2S_MIC_DIN       13
// Speaker/DAC (TX)
#define I2S_SPEAKER_BCLK  17
#define I2S_SPEAKER_LRC   18
#define I2S_SPEAKER_DOUT  19

// === Buffers and Constants ===
#define I2S_MIC_BUFFER_SIZE   1024
#define I2S_SPEAKER_BUFFER_SIZE 512
#define WAV_HEADER_SIZE 44

// === Global State ===
enum State {
  LISTENING,
  PLAYING_AUDIO
};
State currentState = LISTENING;
bool headerParsedForPlayback = false; // Flag to track playback state across loop iterations

WiFiServer server(TCP_PORT);
WiFiClient client;
i2s_port_t i2s_port = I2S_NUM_0;


// --- I2S DRIVER SETUP ---

void setupI2S_Mic() {
  i2s_driver_uninstall(i2s_port);
  Serial.println("Configuring I2S for Microphone (RX)...");
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_RX),
    .sample_rate = 16000,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_32BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = ESP_INTR_FLAG_LEVEL1,
    .dma_buf_count = 8,
    .dma_buf_len = 256,
    .use_apll = false,
    .tx_desc_auto_clear = false,
    .fixed_mclk = 0
  };
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_MIC_BCLK,
    .ws_io_num = I2S_MIC_LRC,
    .data_out_num = I2S_PIN_NO_CHANGE,
    .data_in_num = I2S_MIC_DIN
  };
  i2s_driver_install(i2s_port, &i2s_config, 0, NULL);
  i2s_set_pin(i2s_port, &pin_config);
  i2s_zero_dma_buffer(i2s_port);
}

void setupI2S_Speaker(uint32_t sampleRate) {
  i2s_driver_uninstall(i2s_port);
  Serial.printf("Configuring I2S for Speaker (TX) at %d Hz...\n", sampleRate);
  i2s_config_t i2s_config = {
    .mode = (i2s_mode_t)(I2S_MODE_MASTER | I2S_MODE_TX),
    .sample_rate = sampleRate,
    .bits_per_sample = I2S_BITS_PER_SAMPLE_16BIT,
    .channel_format = I2S_CHANNEL_FMT_ONLY_LEFT,
    .communication_format = I2S_COMM_FORMAT_I2S,
    .intr_alloc_flags = 0,
    .dma_buf_count = 8,
    .dma_buf_len = 64, // ** THE FIX ** Reverted to 64 from 1024 to ensure stability.
    .use_apll = false,
    .tx_desc_auto_clear = true,
    .fixed_mclk = 0
  };
  i2s_pin_config_t pin_config = {
    .bck_io_num = I2S_SPEAKER_BCLK,
    .ws_io_num = I2S_SPEAKER_LRC,
    .data_out_num = I2S_SPEAKER_DOUT,
    .data_in_num = I2S_PIN_NO_CHANGE
  };
  i2s_driver_install(i2s_port, &i2s_config, 0, NULL);
  i2s_set_pin(i2s_port, &pin_config);
}


// --- WAV Playback Logic ---

bool parseWavHeader(uint32_t &sampleRate, uint16_t &bitsPerSample) {
  uint8_t header[WAV_HEADER_SIZE];
  size_t bytesRead = client.readBytes(header, WAV_HEADER_SIZE);
  if (bytesRead != WAV_HEADER_SIZE) {
    Serial.println("Error: Could not read WAV header fully");
    return false;
  }
  if (strncmp((char*)header, "RIFF", 4) != 0 || strncmp((char*)(header + 8), "WAVE", 4) != 0) {
    Serial.println("Error: Invalid WAV header");
    return false;
  }
  sampleRate = header[24] | (header[25] << 8) | (header[26] << 16) | (header[27] << 24);
  bitsPerSample = header[34] | (header[35] << 8);
  uint16_t channels = header[22] | (header[23] << 8);
  Serial.printf("WAV header parsed: rate=%u, bits=%u, channels=%u\n", sampleRate, bitsPerSample, channels);
  if (bitsPerSample != 16 || channels != 1) {
    Serial.println("Error: Unsupported format. Only 16-bit mono is supported.");
    return false;
  }
  return true;
}

void playAudioFromClient() {
    // Ensure stream reads do not block for too long
    client.setTimeout(20); // 20 ms read timeout to keep audio flowing

    if (!headerParsedForPlayback) {
        if (client.available() >= WAV_HEADER_SIZE) {
            uint32_t sampleRate = 0;
            uint16_t bitsPerSample = 0;
            if (parseWavHeader(sampleRate, bitsPerSample)) {
                setupI2S_Speaker(sampleRate);
                headerParsedForPlayback = true;
                Serial.println("Header parsed, starting playback.");
            } else {
                Serial.println("Failed to parse WAV header, closing client.");
                client.stop(); // This will trigger the disconnect logic in the main loop
            }
        }
    } else {
        static uint8_t silence[I2S_SPEAKER_BUFFER_SIZE]; // zero-initialized
        uint8_t buffer[I2S_SPEAKER_BUFFER_SIZE];
        size_t bytes_read = client.readBytes(buffer, I2S_SPEAKER_BUFFER_SIZE);
        const uint8_t* out_ptr = buffer;
        size_t out_len = bytes_read;
        if (bytes_read == 0) {
            // No data arrived within timeout; write a buffer of silence to avoid gaps
            out_ptr = silence;
            out_len = sizeof(silence);
        }

        size_t bytes_written = 0;
        i2s_write(i2s_port, out_ptr, out_len, &bytes_written, portMAX_DELAY);
        // It's okay if bytes_written < out_len occasionally; DMA may be busy
    }
}


// --- Main Setup and Loop ---

void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.print("Connecting to WiFi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());
  server.begin();
  Serial.printf("TCP server started on port %d\n", TCP_PORT);
  setupI2S_Mic();
}

void loop() {
  if (client && !client.connected()) {
    client.stop();
    i2s_stop(i2s_port); // Stop I2S to prevent garbage sound
    Serial.println("Client disconnected. Resetting to LISTENING mode.");
    currentState = LISTENING;
    headerParsedForPlayback = false; // Reset the playback flag
    setupI2S_Mic();
  }

  if (!client) {
    client = server.available();
    if (client) {
      Serial.println("New client connected!");
      currentState = LISTENING;
      headerParsedForPlayback = false; // Ensure flag is reset for new client
      setupI2S_Mic();
    }
    return;
  }
  
  if (currentState == LISTENING) {
    if (client.available() > 0) {
      String command = client.readStringUntil('\n');
      command.trim();
      if (command == "PLAY") {
        Serial.println("Received PLAY command. Switching to audio playback mode.");
        currentState = PLAYING_AUDIO;
        return;
      }
    }
    int32_t buffer[I2S_MIC_BUFFER_SIZE];
    size_t bytes_read = 0;
    i2s_read(i2s_port, (void*)buffer, sizeof(buffer), &bytes_read, (10 / portTICK_PERIOD_MS));
    if (bytes_read > 0) {
      client.write((const uint8_t*)buffer, bytes_read);
    }
    
  } else if (currentState == PLAYING_AUDIO) {
    playAudioFromClient();
  }
}
