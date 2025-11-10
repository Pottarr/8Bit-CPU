# 8Bits CPU Simulation

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

### Instruction Code

#### General Instruction Code

| Opcode| ImmFlag | EditFlag | Rdest | Rsrc1 | Imm/Rsrc2 |
| :----: | :----: | :------: | :---: | :---: | :-------: |
| $AAAAA$ | $B$ | $CCCC$ | $EEE$ | $FFF$ | $GGGGGHHH$ |

Total bits: 20

$DC \rightarrow$ Don't care

#### Instruction Code

##### Do in $ID$

- NOP

##### Do in $EX_{ALU}$

- ADD
- SUB
- MUL
- AND
- OR
- XOR
- NOT

##### Do in $EX_{JUMP}$

- BC
- BZ
- BNZ
- BNG
- B

##### Do in $ME_{Stack}$

- PSH
- POP

##### Do in $ME_{I/O}$

- RD
- WR

##### Do in $ME_{RAM}$

- LD
- ST

##### Done in $ME_{RAM}$

- MOV

### Future Plans

- Implement Software Interrupt

### Contributers

- [Theepakorn Phayonrat 67011352](https://github.com/Pottarr)
- [Chawit Saritdeechaikul 67011093](https://github.com/its-sentral)
