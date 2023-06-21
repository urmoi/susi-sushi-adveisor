# Susi the Sushi Machine - adveisor TUM

![Render of Machine](https://github.com/urmoi/susi-sushi-adveisor/blob/main/susi_sushi_render.png?raw=true)

## Introduction

This is the Codebase for our automated Sushi Machine in regards of the [TU Munich adveisor programm](https://www.ce.cit.tum.de/lsr/lehre/adveisor "TUM adveisor") year 2022/2023 project:

> ### Küchen-Assistent-Roboter | Kitchen-Assistent-Robot

The goal of this project is to build a robot that can assist in the kitchen.
The robot should be able to prepare a meal from start to finish and should be easy to use.

The maschine is 3D printed and motorized, sensorized, and controlled by a Raspberry Pi Zero W.
The schematics are down below, the 3D files will be eventually uploaded to this repository.

---

## Functionality and Features

### Mechanics

> ![Mechanics Animation](https://github.com/urmoi/susi-sushi-adveisor/blob/main/susi_sushi_mechanics.gif?raw=true)

### Functions

> 1. Selection of three different Ingredients
> 2. Automatic Distribution of Sushi Rice
> 3. Automatic Loading of Ingredients
> 4. Automatic Sushi Rolling | Folding Mechanism

### Handling

> #### [Bedienungsanleitung](https://github.com/urmoi/susi-sushi-adveisor/blob/main/Bedienungsanleitung.pdf?raw=true)
>
> - Button Interface with Light Feedback
> - Easy Removing and Cleaning of Dirty Parts

### Codebase

> - Python 3.9 running on a Raspberry Pi Zero W
> - Custom G-code flavored instruction commands (.scode)
> - Custom firmware | interpreter (firmware.py)
> - Config file (.json) to setup the Components
> - Test and Calibrations Scripts (beginning with _) | CLI

---

## Resources

- [Raspberry Pi Pinout](https://pinout.xyz)
- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [How to use a Hall Effect Sensor with the Raspberry Pi](https://www.raspberrypi-spy.co.uk/2015/09/how-to-use-a-hall-effect-sensor-with-the-raspberry-pi/)
- [How to use Stepper Motors with the Raspberry Pi](https://learn.adafruit.com/adafruit-dc-and-stepper-motor-hat-for-raspberry-pi/using-stepper-motors)
- [How to use Servo Motos with the Raspberry Pi](https://learn.adafruit.com/adafruit-16-channel-pwm-servo-hat-for-raspberry-pi/using-the-python-library)

## Libraries

- [adafruit-blinka](https://github.com/adafruit/Adafruit_Blinka)
- [adafruit-circuitpython-motorkit](https://github.com/adafruit/Adafruit_CircuitPython_MotorKit)
- [adafruit-circuitpython-servokit](https://github.com/adafruit/Adafruit_CircuitPython_ServoKit)
- [adafruit-circuitpyrhon-vl53l4cd](https://github.com/adafruit/Adafruit_CircuitPython_VL53L4CD)
- [getch](https://github.com/joeyespo/py-getch)

## Components

- [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
- [Adafruit DC & Stepper Motor HAT & Bonnet for Raspberry Pi](https://www.adafruit.com/product/4280)
- [Adafruit 16-Channel PWM/Servo HAT & Bonnet for Raspberry Pi](https://www.adafruit.com/product/2327)
- [Adafruit VL53L4CD Time of Flight Distance Sensor - ~50 to 4000mm](https://www.adafruit.com/product/3317)
- Servo Motors (continuous rotation and 180° standard)
- Stepper Motor (e.g. NEMA 14)
- Hall Sensors (e.g. A3144 with an 10kΩ resistor)

![Schematics Fritzing](https://github.com/urmoi/susi-sushi-adveisor/blob/main/schematics_fritzing.png?raw=true)
