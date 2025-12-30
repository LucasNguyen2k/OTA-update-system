# 🚗Software-Defined Vehicle (SDV) – Vehicle Signal Simulation and Validation

## Overview
Built a software-defined vehicle simulation platform with signal services, OTA update flows, diagnostics, and CI-driven safety validation

### This SDV project series demonstrates:
- A signal publisher (speed, RPM, battery)
- A consumer (ADAS / monitoring service)
- Validation & fault injection
- CI tests for safety rules
- Test-driven development
- Automation and Mocking

### The Vehicle Signal Service focuses on:
- Signal definitions (speed, brake, gear, battery)
- CAN-like message simulation (no hardware)
- Signal decoder / encoder
- Fault injection (dropped signals, invalid values)

## Tech Stack & Skills
- Python 3.10+
- dataclasses
- pytest
- Automotive signals
- Middleware thinking
- Simulation over hardware
- Safety-aware logic

## Project Structure
```text

SDVProjects/
└── vehicle-signal-simulator/
    │   README.md
    │   requirements.txt
    │
    ├───src
    │   │   signals.py
    │   │   providers.py
    │   │   processor.py
    │   │   validator.py
    │   │   can_bus.py
    │   │   message.py
    │   │   signal_service.py
    │   │   service.py
    │
    └───tests
        │   test_processor.py
        │   test_providers.py
        │   test_signals.py
        │   test_validator.py
        │   test_can_bus.py
        │   test_signal_service.py
        │   test_service.py
```


## Vehicle State Machine Diagram

### Vehicle Signal Validator Logic
```
Vehicle Signals  →  Validator  →  State Processor  →  Vehicle State
```

### SDV Architecture Layers 
```
Apps / Cloud / HMI Features
        ↕
Vehicle State / Domain Logic
        ↕
Signal Abstraction Layer
        ↕
CAN Message 
        ↕
CAN Bus / Vehicle Network
```

### CAN Message Simulation
```
- Message ID 0x100
- Byte 0 = vehicle speed (km/h)
```


## Installation
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -r requirements.txt

## Outputs:
None

## Testing
```
python -m pytest
```