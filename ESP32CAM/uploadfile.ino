#include <WiFi.h>
#include <HTTPClient.h>
#include <FS.h>
#include <SPIFFS.h>
#include <Arduino.h>
#include "esp_camera.h"

// WiFi credentials
const char* ssid = "*****";
const char* password = "******";

// Server URL
const char* serverUrl = "https://server-fastapi-2b0eb22f2d67.herokuapp.com/";

// Define camera model
#define CAMERA_MODEL_AI_THINKER

#if defined(CAMERA_MODEL_AI_THINKER)
  #define PWDN_GPIO_NUM    32
  #define RESET_GPIO_NUM   -1
  #define XCLK_GPIO_NUM    0
  #define SIOD_GPIO_NUM    26
  #define SIOC_GPIO_NUM    27
  #define Y9_GPIO_NUM      35
  #define Y8_GPIO_NUM      34
  #define Y7_GPIO_NUM      39
  #define Y6_GPIO_NUM      36
  #define Y5_GPIO_NUM      21
  #define Y4_GPIO_NUM      19
  #define Y3_GPIO_NUM      18
  #define Y2_GPIO_NUM      5
  #define VSYNC_GPIO_NUM   25
  #define HREF_GPIO_NUM    23
  #define PCLK_GPIO_NUM    22
#endif

void setup() {
    Serial.begin(115200);
    
    // Connect to Wi-Fi
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    // Camera configuration
    Serial.println("config");
    camera_config_t config;
      config.ledc_channel = LEDC_CHANNEL_0;
      config.ledc_timer = LEDC_TIMER_0;
      config.pin_d0 = Y2_GPIO_NUM;
      config.pin_d1 = Y3_GPIO_NUM;
      config.pin_d2 = Y4_GPIO_NUM;
      config.pin_d3 = Y5_GPIO_NUM;
      config.pin_d4 = Y6_GPIO_NUM;
      config.pin_d5 = Y7_GPIO_NUM;
      config.pin_d6 = Y8_GPIO_NUM;
      config.pin_d7 = Y9_GPIO_NUM;
      config.pin_xclk = XCLK_GPIO_NUM;
      config.pin_pclk = PCLK_GPIO_NUM;
      config.pin_vsync = VSYNC_GPIO_NUM;
      config.pin_href = HREF_GPIO_NUM;
      config.pin_sccb_sda = SIOD_GPIO_NUM;
      config.pin_sccb_scl = SIOC_GPIO_NUM;
      config.pin_pwdn = PWDN_GPIO_NUM;
      config.pin_reset = RESET_GPIO_NUM;
      config.xclk_freq_hz = 20000000;
      config.pixel_format = PIXFORMAT_JPEG;
      if(psramFound()) {
        config.frame_size = FRAMESIZE_UXGA;
        config.jpeg_quality = 10;
        config.fb_count = 2;
      } else {
        config.frame_size = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
      }
    // Initialize the camera
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK) {
        Serial.printf("Camera init failed with error 0x%x", err);
        return;
    }
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    captureAndUpload();
  }
  delay(2000);  // Capture every 10 seconds
}

void captureAndUpload() {
  // Capture the image
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Camera capture failed");
    return;
  }

  // Prepare the HTTP client
  HTTPClient http;
  http.begin(serverUrl);

  // Prepare the multipart boundary
  String boundary = "----ESP32Boundary";
  http.addHeader("Content-Type", "multipart/form-data; boundary=" + boundary);

  // Prepare the form data
  String bodyStart = "--" + boundary + "\r\n" +
                     "Content-Disposition: form-data; name=\"file\"; filename=\"image.jpg\"\r\n" +
                     "Content-Type: image/jpeg\r\n\r\n";
  String bodyEnd = "\r\n--" + boundary + "--\r\n";

  // Calculate the total size of the payload
  size_t totalSize = bodyStart.length() + fb->len + bodyEnd.length();

  // Allocate memory for the entire request
  uint8_t *requestData = (uint8_t *)malloc(totalSize);

  // Copy the form data parts into the request buffer
  memcpy(requestData, bodyStart.c_str(), bodyStart.length());
  memcpy(requestData + bodyStart.length(), fb->buf, fb->len);
  memcpy(requestData + bodyStart.length() + fb->len, bodyEnd.c_str(), bodyEnd.length());

  // Send the POST request
  int httpResponseCode = http.POST(requestData, totalSize);

  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Response from server:");
    Serial.println(response);
  } else {
    Serial.printf("Error code: %d\n", httpResponseCode);
  }

  // Free the allocated memory
  free(requestData);
  esp_camera_fb_return(fb);

  http.end();
}
