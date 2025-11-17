# 8Bits CPU Simulation

This project was create as a final project for the Computer
Architecture and Organization class of B.Eng. @ KMITL  
For marking, please go to [this branch](https://github.com/Pottarr/8Bit-CPU/tree/Checkpoint).
Other branches are for continuous development after the project was
finished.

## Program used

- [Digital](https://github.com/hneemann/Digital)

## [Documentation](doc/Documentation.pdf)

## Specification

### Overview

- 8 bits size memory
- 8 accessible registers `R0` - `R7`
- 20 bits size instruction
- Support 5 Stages of Pipeline
- Provided Solution for Pipeline Hazards
- Support Stack
- Support 8 bits I/O
- Branch Prediction: Assume Not Taken as Default
- Provided Assembler as [compiler.py](test/compiler.py)

### Components

- PC (Program Counter)
- IR (Instruction Register: Using ROM (Read Only Memory))
- RAM (Random Access Memory)
- CU (Control Unit)
- Register File
- ALU (Arithmetic and Logic Unit)
    - Adder
    - Subtractor
    - Multiplier
    - AND
    - OR
    - XOR
    - NOT
- Flags Register
- Forward Register
- Stack Pointer Register

### Future Plans

- Implement Software Interrupt
- Expand to 32 bits

### [Successor repository](https://github.com/Pottarr/I-ASSUME-CPU)

### Contributers

- [Theepakorn Phayonrat 67011352](https://github.com/Pottarr)
- [Chawit Saritdeechaikul 67011093](https://github.com/its-sentral)
