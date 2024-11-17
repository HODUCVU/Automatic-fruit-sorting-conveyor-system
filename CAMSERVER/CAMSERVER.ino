// https://github.com/yoursunny/esp32cam
#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>

#define WIFI_SSID "************"
#define WIFI_PASS "************"

WebServer captureServer(80);   // Server for image capture
WebServer streamServer(81);    // Server for MJPEG streaming

static auto hiRes = esp32cam::Resolution::find(800, 600);

void serveJpg() {
  auto frame = esp32cam::capture();
  if (frame == nullptr) { 
    Serial.println("CAPTURE FAIL");
    captureServer.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));
 
  captureServer.setContentLength(frame->size());
  captureServer.send(200, "image/jpeg");
  WiFiClient client = captureServer.client();
  frame->writeTo(client);
}

void handleJpgHi() {
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}

void handleMjpeg() {
  WiFiClient client = streamServer.client();
  String response = "HTTP/1.1 200 OK\r\n"
                    "Content-Type: multipart/x-mixed-replace; boundary=frame\r\n"
                    "\r\n";
  client.print(response);
  
  while (client.connected()) {
    auto frame = esp32cam::capture();
    if (frame == nullptr) {
      Serial.println("CAPTURE FAIL");
      break;
    }
    client.printf("--frame\r\n"
                  "Content-Type: image/jpeg\r\n"
                  "Content-Length: %d\r\n\r\n", frame->size());
    frame->writeTo(client);
    client.print("\r\n");
    delay(50); // Adjust delay for smooth streaming
  }
}

void captureTask(void *pvParameters) {
  captureServer.on("/cam-hi.jpg", handleJpgHi);
  captureServer.begin();
  for (;;) {
    captureServer.handleClient();
//    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void streamTask(void *pvParameters) {
  streamServer.on("/monitor", []() {
    handleMjpeg();
  });
  streamServer.begin();
  for (;;) {
    streamServer.handleClient();
//    vTaskDelay(10 / portTICK_PERIOD_MS);
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println();

  using namespace esp32cam;
  Config cfg;
  cfg.setPins(pins::AiThinker);
  cfg.setResolution(hiRes);
  cfg.setBufferCount(2);
  cfg.setJpeg(80);

  bool ok = Camera.begin(cfg);
  Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("Capture server: http://");
  Serial.print(WiFi.localIP());
  Serial.println("/cam-hi.jpg");
  
  Serial.print("Stream server: http://");
  Serial.print(WiFi.localIP());
  Serial.println(":81/monitor");

  xTaskCreatePinnedToCore(captureTask, "Capture Task", 4096, NULL, 1, NULL, 0);  // Core 0
  xTaskCreatePinnedToCore(streamTask, "Stream Task", 4096, NULL, 1, NULL, 1);    // Core 1
}

void loop() {}