# Smart Samovar Controller (Arduino Uno)

An embedded temperature control and dispensing system built on the **Arduino Uno**. It uses a **PT100** RTD sensor paired with a **MAX31865** amplifier (over SPI) to monitor water temperature, controls a heating element and electric valve via relays, and displays real-time system status on an **SSD1306 OLED** screen.

![Circuit Schematic](./circuit-schematic.jpg)

## Features
- **High-Precision Temperature Sensing:** Reads temperature from a 4-wire PT100 RTD sensor using the MAX31865 converter (`RREF = 430.0 Ω`, `RNOMINAL = 100.0 Ω`) and outputs values to both the OLED display and Serial Monitor (`9600 baud`).
- **Automated Heating Control:**
  - **Below `100°C`:** Activates the heating stage (`heater` pin `LOW`), lights the red status LED, and displays `warming up!`.
  - **`100°C` and above:** Switches the heating state (`heater` pin `HIGH`), turns on the blue status LED, and displays `ready to drink`.
- **Push-Button Valve Dispensing:** Pressing the control button activates the electric water valve and blinks the green LED 6 times (`50 ms` intervals).
- **Sensor Fault Detection:** Validates temperature readings and displays `Error: Sensor` if values are `NaN` or outside the `-100°C` to `500°C` range.

## Hardware & Pinout

| Component / Signal | Arduino Pin / Address | Notes |
| :--- | :--- | :--- |
| **MAX31865 (CS, DI, DO, CLK)** | `D10, D11, D12, D13` | Software/Hardware SPI interface (4-wire PT100 mode) |
| **OLED Display (128x64)** | `A4 (SDA), A5 (SCL)` | I2C address `0x3C`, display rotation set to `2` |
| **Heater Relay (`R_H`)** | `D9` | Digital output |
| **Electric Valve Relay (`R_V`)** | `D8` | Digital output |
| **Blue LED (`D1`)** | `D7` | Ready indicator (`>= 100°C`) |
| **Red LED (`D2`)** | `D6` | Warming up indicator (`< 100°C`) |
| **Green LED (`D3`)** | `D5` | Dispensing indicator |
| **Dispense Button** | `D4` | Configured with `INPUT_PULLUP` (active `LOW`) |

## Getting Started
1. Install the required libraries via the **Arduino IDE Library Manager**:
   - `Adafruit MAX31865 library`
   - `Adafruit SSD1306`
   - `Adafruit GFX Library`
2. Wire the components according to `circuit-schematic.jpg` (or load the design into Proteus for simulation).
3. Open `samovar_controller.ino` in Arduino IDE, select **Arduino Uno**, and upload the sketch.