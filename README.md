# Micro:bit - Grove Examples

![Splash](splash.png)

## Introduction

This repository contains examplea Micropython programs demonstrating how to use various Grove components with the BBC Micro:bit microcontroller.

## Grove Components

The library covers the following Grove components

| Component                                                  |                                                           | SeeedStudio                                                                                                         | Example  |
| ---------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------- |
| OLED Display 0.66" (SSD1306)                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-OLED-Display-0-66-SSD1306-v1-0-p-5096.html)                             |          |
| OLED Yellow&Blue Display 0.96 (SSD1315)                    |                                                           | [Go Here](https://www.seeedstudio.com/Grove-OLED-Yellow-Blue-Display-0-96-SSD1315-V1-0-p-5010.html)                 |          | 
| Analog Microphone (MEMS)                                   |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Analog-Microphone-p-4593.html)                                          |          |
| Ultrasonic Distance Sensor                                 |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Ultrasonic-Distance-Sensor.html)                                        |          |
| Passive Buzzer                                             | ![Passive Buzzer](img/passive-buzzer.png)                 | [Go Here](https://www.seeedstudio.com/Grove-Passive-Buzzer-p-4525.html)                                             | [Go Here](src/passive-buzzer.py)        |
| Piezo Buzzer/Active Buzzer                                 |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Buzzer.html)                                                            |          |
| LED (Blue, Red, Green, White)                              | ![LED](img/led.png)                                       | [Go Here](https://www.seeedstudio.com/Grove-LED-Pack-p-4364.html)                                                   | [Go Here](src/led.py)                   |
| 3-Axis Digital Accelerometer(±1.5g)                        |                                                           | [Go Here](https://www.seeedstudio.com/Grove-3-Axis-Digital-Accelerometer-1-5g.html)                                 |          |
| Magnetic Switch                                            | ![Magnetic Switch](img/magnetic-switch.png)               | [Go Here](https://www.seeedstudio.com/Grove-Magnetic-Switch.html)                                                   | [Go Here](src/magnetic-switch.py)       |
| Tilt Switch                                                | ![Tilt Switch](img/tilt-switch.png)                       | [Go Here](https://www.seeedstudio.com/Grove-Tilt-Switch.html)                                                       | [Go Here](src/tilt-switch.py)           |
| Relay                                                      | ![Relay](img/relay.png)                                   | [Go Here](https://www.seeedstudio.com/Grove-Relay.html)                                                             | [Go Here](src/relay.py)                 |
| Water Sensor                                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Water-Sensor.html)                                                      |          |
| Temperature Sensor                                         |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Temperature-Sensor.html)                                                |          |
| Temperature & Humidity Sensor (High-Accuracy & Mini)       |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-High-Accuracy-Mini.html)                    |          |
| AHT20 I2C Industrial Grade Temperature and Humidity Sensor | ![AHT20](img/aht20.png)                                   | [Go Here](https://www.seeedstudio.com/Grove-AHT20-I2C-Industrial-grade-temperature-and-humidity-sensor-p-4497.html) | [Go Here](src/aht.py)                   |
| Temperature & Humidity Sensor V2.0 (DHT20)                 |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-V2-0-DHT20-p-4967.html)                     |          |
| Temperature & Humidity Sensor (DHT11)                      |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-DHT11.html)                                 |          |
| Temperature & Humidity Sensor Pro (DHT22/AM2302)           | ![Temp & Hum Sensor Pro](img/tem-hum-sensor-pro.png)      | [Go Here](https://www.seeedstudio.com/Grove-Temperature-Humidity-Sensor-Pro-AM2302-DHT22.html)                      |          |
| Vibration Motor                                            | ![Vibration Motor](img/vibration-motor.png)               | [Go Here](https://www.seeedstudio.com/Grove-Vibration-Motor.html)                                                   | [Go Here](src/vibration-motor.py)       |
| Thumb Joystick                                             |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Thumb-Joystick.html)                                                    |          |
| Soil Moisture Sensor                                       |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Moisture-Sensor.html)                                                   |          |
| Slide Potentiometer                                        | ![Slide Potentiometer](img/sliding-potentiometer.png)     | [Go Here](https://www.seeedstudio.com/Grove-Slide-Potentiometer.html)                                               | [Go Here](src/sliding_potentiometer.py) |
| Rotary Angle Sensor                                        | ![Rotary Angle Sensor](img/rotary-angle-sensor.png)       | [Go Here](https://www.seeedstudio.com/Grove-Rotary-Angle-Sensor-P.html)                                             | [Go Here](src/rotary-angle-sensor.py)   |
| Encoder                                                    | ![Encoder](img/encoder.png)                               | [Go Here](https://www.seeedstudio.com/Grove-Encoder.html)                                                           | [Go Here](src/encoder.py)             
| Sound Sensor/Noise Detector                                |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Loudness-Sensor.html)                                                   |          |
| Speaker Plus                                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Speaker-Plus-p-4592.html)                                               |          |
| Speaker                                                    | ![Speaker](img/speaker.png)                               | [Go Here](https://www.seeedstudio.com/Grove-Speaker-p-1445.html)                                                    | [Go Here](src/speaker.py)               |
| Flame Sensor                                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Flame-Sensor.html)                                                      |          |
| 4-Digit Display                                            |                                                           | [Go Here](https://www.seeedstudio.com/Grove-4-Digit-Display.html)                                                   |          |
| MOSFET                                                     |                                                           | [Go Here](https://www.seeedstudio.com/Grove-MOSFET.html)                                                            |          |
| Infrared Reflective Sensor v1.2                            |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Infrared-Reflective-Sensor-v1-2.html)                                   |          |
| Light Sensor (P) v1.1                                      |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Light-Sensor-P-v1-1.html)                                               |          |
| Temperature and Barometer Sensor                           |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Barometer-Sensor-BMP280.html)                                           |          |
| LED Button (Red, Blue, Yellow)                             | ![LED Button](img/led-button.png)                         | [Go Here](https://www.seeedstudio.com/Grove-Red-LED-Button.html)                                                    | [Go Here](src/dual-button.py)           |
| Variable Color LED V1.1                                    | ![Variable Color LED](img/variable-color-led.png)         | [Go Here](https://www.seeedstudio.com/Grove-Variable-Color-LED-V1-1.html)                                           | [Go Here](src/variable-color-led.py)    |
| I2C Motor Driver (TB6612FNG)                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-I2C-Motor-Driver-TB6612FNG-p-3220.html)                                 |          |
| PIR Motion Sensor                                          |                                                           | [Go Here](https://www.seeedstudio.com/Grove-PIR-Motion-Sensor.html)                                                 |          |
| mini PIR motion sensor                                     |                                                           | [Go Here](https://www.seeedstudio.com/Grove-mini-PIR-motion-sensor-p-2930.html)                                     |          |
| Adjustable PIR Motion Sensor                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Adjustable-PIR-Motion-Sensor.html)                                      |          |
| Dual Button                                                | ![Dual Button](img/dual-button.png)                       | [Go Here](https://www.seeedstudio.com/Grove-Dual-Button-p-4529.html)                                                | [Go Here](src/dual-button.py)           |
| Button                                                     | ![Button](img/button.png)                                 | [Go Here](https://www.seeedstudio.com/buttons-c-928/Grove-Button.html)                                              | [Go Here](src/button.py)                |
| Switch(P)                                                  | ![Switch-P](img/switch-p.png)                             | [Go Here](https://www.seeedstudio.com/Grove-Switch-P.html)                                                          | [Go Here](src/switch-p.py)              |
| Purple LED (3mm)                                           |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Purple-LED-3mm.html)                                                    |          |
| Light Sensor                                               |                                                           | [Go Here](https://www.seeedstudio.com/Grove-Light-Sensor-p-746.html)                                                |          |
| Touch Sensor                                               | ![Touch Sensor](img/touch.png)                            | [Go Here](https://www.seeedstudio.com/Grove-Touch-Sensor.html)                                                      | [Go Here](src/touch.py)                 |
| Multi Color Flash LED                                      | ![Multi Color Flash LED](img/multi-color-flash-led.png)   | [Go Here](https://www.seeedstudio.com/Grove-Multi-Color-Flash-LED-5mm.html)                                         | [Go Here](src/led.py)                   |
| 6 Poisition Dip Switch                                     | ![6 Position Dip Switch](img/6-position-dip-switch.png)   | [Go Here](https://www.seeedstudio.com/Grove-6-Position-DIP-Switch.html)                                             | [Go Here](src/6-position-dip-switch.py) |
| Gesture                                                    | ![Gesture](img/gesture.png)                               | [Go Here](https://wiki.seeedstudio.com/Grove-Gesture_v1.0/)                                                         | [Go Here](src/gesture.py)               | | LCD 16x2                                                   | ![LCD](img/lcd16x2.png)                                   | [Go Here](https://wiki.seeedstudio.com/Grove-16x2_LCD_Series/)                                                      | [Go Here](src/lcd16x2.py)               | 

## Sundry Folder

## Work In Progress (wip) Folder
