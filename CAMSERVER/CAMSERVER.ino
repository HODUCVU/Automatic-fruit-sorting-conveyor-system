#include <WebServer.h>
#include <WiFi.h>
#include <esp32cam.h>


//#define BLYNK_TEMPLATE_ID "TMPL6k07VM3Nj"
//#define BLYNK_TEMPLATE_NAME "Monitoring"
//#define BLYNK_AUTH_TOKEN "UaWBXAAtqJJsZwIt9bWw6wlKbYZXlJjM"

//#define BLYNK_TEMPLATE_ID "TMPL6jDuSVjPI"
//#define BLYNK_TEMPLATE_NAME "PBL5"
//#define BLYNK_AUTH_TOKEN "y1uPz6lIRsVM8OVFa0u6EC3UzsNnCQL6"

#include <BlynkSimpleEsp32.h>

//const char* WIFI_SSID = "Zone Six Phu";
//const char* WIFI_PASS = "19phamnhuxuong";

const char* WIFI_SSID = "Realmi";
 const char* WIFI_PASS = "20102002";

//const char* WIFI_SSID = "CUONGTRAN";
//const char* WIFI_PASS = "1234567890";


WebServer server(80);
 
 
static auto loRes = esp32cam::Resolution::find(320, 240);
static auto midRes = esp32cam::Resolution::find(350, 530);
static auto hiRes = esp32cam::Resolution::find(800, 600);
void serveJpg()
{
  auto frame = esp32cam::capture();
  if (frame == nullptr) { 
    Serial.println("CAPTURE FAIL");
    server.send(503, "", "");
    return;
  }
  Serial.printf("CAPTURE OK %dx%d %db\n", frame->getWidth(), frame->getHeight(),
                static_cast<int>(frame->size()));
 
  server.setContentLength(frame->size());
  server.send(200, "image/jpeg");
  WiFiClient client = server.client();
  frame->writeTo(client);
}
 
void handleJpgLo()
{
  if (!esp32cam::Camera.changeResolution(loRes)) {
    Serial.println("SET-LO-RES FAIL");
  }
  serveJpg();
}
 
void handleJpgHi()
{
  if (!esp32cam::Camera.changeResolution(hiRes)) {
    Serial.println("SET-HI-RES FAIL");
  }
  serveJpg();
}
 
void handleJpgMid()
{
  if (!esp32cam::Camera.changeResolution(midRes)) {
    Serial.println("SET-MID-RES FAIL");
  }
  serveJpg();
}

void handleMjpeg() {
  WiFiClient client = server.client();
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
    
    delay(50); // Adjust delay as needed for smooth streaming
  }
}

//void blynkTask(void *pvParameters) {
//  Blynk.begin(BLYNK_AUTH_TOKEN, WiFi.SSID().c_str(), WiFi.psk().c_str());
//  while (true) {
//    Blynk.run(); // Run Blynk events
////    Serial.println("Bynk runniing");
//    vTaskDelay(10/ portTICK_PERIOD_MS);   // Small delay to prevent watchdog reset
//  }
//} 

void serverhanlder(void *pvParameters) {
  while(true) {
    server.handleClient(); 
    vTaskDelay(10/ portTICK_PERIOD_MS);
  }
}
void  setup(){
  Serial.begin(115200);
  Serial.println();
  {
    using namespace esp32cam;
    Config cfg;
    cfg.setPins(pins::AiThinker);
    cfg.setResolution(hiRes);
    cfg.setBufferCount(2);
    cfg.setJpeg(80);
 
    bool ok = Camera.begin(cfg);
    Serial.println(ok ? "CAMERA OK" : "CAMERA FAIL");
  }
  WiFi.persistent(false);
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }
  Serial.print("http://");
  Serial.println(WiFi.localIP());
  Serial.println("  /cam-lo.jpg");
  Serial.println("  /cam-hi.jpg");
  Serial.println("  /cam-mid.jpg");
  Serial.println("  /mjpeg");
  
  server.on("/cam-lo.jpg", handleJpgLo);
  server.on("/cam-hi.jpg", handleJpgHi);
  server.on("/cam-mid.jpg", handleJpgMid);
  server.on("/mjpeg", handleMjpeg);
  
  server.begin();
  // Create the Blynk task and pin it to Core 1
//  xTaskCreatePinnedToCore(blynkTask, "Blynk Task", 4096, NULL, 1, NULL, 1); // Core 1
  xTaskCreatePinnedToCore(serverhanlder, "server hanlder", 4096, NULL, 1, NULL, 0); // Core 0
}
 
void loop()
{
//  server.handleClient();
}
