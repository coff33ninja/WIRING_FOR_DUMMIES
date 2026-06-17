# ESP32 Web Server — Toggle LED from Browser

## What You'll Build

An ESP32 that hosts a **WiFi web page**. When you open the page in a browser, you see a button. Click it — an LED turns on. Click it again — it turns off. This is the foundation for every IoT project (sensor dashboards, remote control, smart home).

## How It Works

```
                  ┌─────────────────┐
  Browser ──WiFi──┤    ESP32        │
  (phone,         │  ┌───────────┐  │
   laptop)        │  │ Web server │  │
                  │  │ listens on │  │
                  │  │ port 80    │  │
                  │  └───────────┘  │
                  │       │         │
                  │     GPIO 2      │
                  │       │         │
                  │    [330Ω]       │
                  │       │         │
                  │      LED ── GND │
                  └─────────────────┘
```

The ESP32 acts as a **web server**. Your browser connects to its IP address, requests a page, and the ESP32 sends HTML. When you click the button, the browser sends a request to `/led/on` or `/led/off`, and the ESP32 toggles the GPIO.

## Parts List

| Part | Qty |
|------|-----|
| ESP32 dev board | 1 |
| LED (any color) | 1 |
| 330Ω resistor | 1 |
| Breadboard + jumper wires | 1 |

## Wiring

Simple — just one LED on GPIO 2:

```
ESP32                  Breadboard
─────                  ──────────
GPIO 2 ────────────────[330Ω]──┬── LED (+) ──── LED (−) ──── GND
                               │
                          (longer leg)
```

GPIO 2 is the ESP32's built-in LED pin on most boards (labeled "LED" or "D2"). The 330Ω resistor limits current to ~10mA.

## Code

### 1. Complete Sketch

```cpp
#include <WiFi.h>
#include <WebServer.h>

// Replace with your WiFi credentials
const char* ssid = "YOUR_WIFI_SSID";
const char* password = "YOUR_WIFI_PASSWORD";

WebServer server(80);
const int ledPin = 2;
bool ledState = LOW;

void handleRoot() {
  String html = R"rawliteral(
<!DOCTYPE html>
<html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: sans-serif; text-align: center; padding: 40px; }
    button {
      font-size: 24px; padding: 16px 40px;
      background: #ff8800; color: white; border: none; border-radius: 8px;
      cursor: pointer; margin: 20px;
    }
    button:hover { background: #e67700; }
    .on { background: #00aa00; }
    .off { background: #cc0000; }
  </style>
</head>
<body>
  <h1>ESP32 LED Control</h1>
  <p>LED is <strong>)rawliteral";
  html += ledState ? "ON" : "OFF";
  html += R"rawliteral(</strong></p>
  <a href="/toggle"><button class=")rawliteral";
  html += ledState ? "off" : "on";
  html += R"rawliteral(">)rawliteral";
  html += ledState ? "Turn OFF" : "Turn ON";
  html += R"rawliteral(</button></a>
</body>
</html>
)rawliteral";
  server.send(200, "text/html", html);
}

void handleToggle() {
  ledState = !ledState;
  digitalWrite(ledPin, ledState);
  handleRoot();  // Refresh page with updated state
}

void setup() {
  Serial.begin(115200);
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nConnected! IP: " + WiFi.localIP().toString());

  server.on("/", handleRoot);
  server.on("/toggle", handleToggle);
  server.begin();
  Serial.println("Server started");
}

void loop() {
  server.handleClient();
}
```

### 2. Upload and Find the IP

1. Set your WiFi SSID and password in the code
2. Upload to ESP32
3. Open **Serial Monitor** (115200 baud)
4. Wait for: `Connected! IP: 192.168.x.x`
5. Open that IP address in your browser

## What Each Part Does

| Code section | What it does |
|-------------|-------------|
| `WiFi.begin(ssid, password)` | Connects to your WiFi network |
| `WiFi.localIP()` | Gets the ESP32's IP address on your network |
| `WebServer server(80)` | Creates an HTTP server on port 80 (the default web port) |
| `server.on("/", handleRoot)` | When browser requests `/`, run `handleRoot()` |
| `server.on("/toggle", handleToggle)` | When browser requests `/toggle`, toggle the LED |
| `server.handleClient()` | Checks for incoming browser requests (call in loop) |
| `server.send(200, "text/html", html)` | Sends HTTP response (200 = OK) with HTML content |

## Making It Useful — Add a Sensor Reading

Once you have the web server, adding sensor data is a small change:

```cpp
float temperature = 25.3;

void handleRoot() {
  // In the HTML:
  // <p>Temperature: <strong>%TEMP%</strong> &deg;C</p>

  String html = pageTemplate;
  html.replace("%TEMP%", String(temperature));
  server.send(200, "text/html", html);
}
```

Or add a **JSON endpoint** for JavaScript to fetch:

```cpp
void handleData() {
  String json = "{ \"temp\": " + String(temperature) + " }";
  server.send(200, "application/json", json);
}
```

## Troubleshooting

| Problem | Likely cause | Fix |
|---------|-------------|-----|
| ESP32 doesn't connect to WiFi | Wrong SSID or password | Double-check credentials (case-sensitive) |
| ESP32 doesn't connect to WiFi | 2.4GHz only — ESP32 doesn't support 5GHz | Make sure your WiFi is 2.4GHz |
| ESP32 connects but page doesn't load | Wrong IP address | Check Serial Monitor for correct IP |
| Page loads but toggle doesn't work | Browser cached old HTML | Hard refresh (Ctrl+F5) or open in incognito |
| Page loads, toggle works, then stops | `server.handleClient()` not in loop | Make sure you call it in `loop()` |
| ESP32 crashes / resets when page loads | Out of memory (HTML too big) | Move HTML to PROGMEM or use smaller page |
| Page is slow to load | DNS resolution timeout | Use IP address directly instead of hostname |

## Going Further

| Feature | How |
|---------|-----|
| **Multiple LEDs** | Add more GPIO pins and `/led/2/on` style routes |
| **Slider control** | Add an HTML `<input type="range">` and `/pwm?value=128` route |
| **Auto-refresh** | Add `<meta http-equiv="refresh" content="5">` in the HTML head |
| **AJAX update** | Use `fetch('/data')` in JavaScript to update without page reload |
| **WiFi Manager** | Use the WiFiManager library to let users set WiFi without re-flashing |
| **OTA updates** | Add ArduinoOTA to upload new code over WiFi |
| **mDNS** | `MDNS.begin("esp-led")` → access at `http://esp-led.local/` instead of IP |

## Quick Reference

```
Core loop:
  setup():
    WiFi.begin(ssid, password)
    server.on("/path", handler)
    server.begin()

  loop():
    server.handleClient()   // Required! Handles incoming requests

Handler sends:
  server.send(code, type, content)
  Example: server.send(200, "text/html", "<h1>Hello</h1>")

Common routes:
  / → main page
  /toggle → toggle output
  /led/on → turn on
  /led/off → turn off
  /data → JSON sensor readings (for JS fetch)

Requirements:
  ESP32 must be on same WiFi network as browser
  ESP32 only supports 2.4GHz WiFi (not 5GHz)
  Port 80 must not be blocked by your router (usually open)
```

## See Also

- [wireless_technologies](/fundamentals/wireless_technologies)
- [reading-schematics](/fundamentals/reading-schematics)
- [multimeter](/fundamentals/multimeter)
- [gpio-pins](/fundamentals/gpio-pins)
- [power-batteries](/fundamentals/power-batteries)
