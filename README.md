# Multi-MCU Embedded Systems Projects

A collection of embedded systems projects demonstrating hands-on development across different microcontroller architectures, programming languages, and hardware communication protocols (**SPI**, **I2C**, digital I/O, and actuator control).

## Repository Structure

| Project Directory | Microcontroller | Language / Framework | Key Components & Protocols |
| :--- | :--- | :--- | :--- |
| [`samovar-controller-arduino/`](./samovar-controller-arduino) | **Arduino Uno** (ATmega328P) | C++ (Arduino Framework) | PT100 RTD, MAX31865 (SPI), SSD1306 OLED (I2C), Relays |
| [`digital-distance-meter-pico/`](./digital-distance-meter-pico) | **Raspberry Pi Pico** (RP2040) | MicroPython | VL53L0X ToF Sensor (I2C1), SSD1306 OLED (I2C0), Push Button |

## Highlights
- **Cross-Platform Development:** Implementing real-time sensor polling, display rendering, and state control in both compiled C++ and MicroPython.
- **Communication Protocols:** Practical interfacing using SPI and dual-bus I2C configurations.
- **Hardware & Simulation:** Includes circuit schematics and breadboard hardware prototypes.