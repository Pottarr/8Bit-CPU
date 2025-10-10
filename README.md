# 8Bits CPU Simulation
- MUL

## Program used

- [Digital](https://github.com/hneemann/Digital)

## [Documentation](doc/Documentation.pdf)

## Plan

### Overview

- 8 bits size registers
- 8 accessible registers `R0` - `R7`
- At most 16 Opcodes

### Components checklist

- [ ] PC
- [ ] ROM
- [ ] RAM
- [ ] IR
- [ ] CU
- [ ] ALU
    - [x] Adder
    - [x] Subtractor
    - [x] Multiplier
    - [x] Divisor : Used Built-in
    - [ ] Adaptation with CPSR
- [ ] CPSR (Flags Register)

### Instruction Code

#### General Instruction Code

| Flags | ImmArg | OpCode | EditFlag | Rdest | Rsrc | Imm |
| :---: | :----: | :----: | :------: | :---: | :--: | :-: |
| $A_{1}A_{2}A_{3}A_{4}$ | $0$ | $CCCC$ | $D$ | $EEE$ | $FFF$ | $GGGGGGGG$ |

Total bits: 24
- $A_{n}$
    - $A_{1} \rightarrow$ Zero Flag
    - $A_{2} \rightarrow$ Signed Flag
    - $A_{3} \rightarrow$ Carry Flag
    - $A_{4} \rightarrow$ Overflow Flag

#### Memory Management Instruction Code

- MOV
- LDR
- STR

| Flags | ImmArg | OpCode | EditFlag | Rdest | Rsrc | Imm |
| :---: | :----: | :----: | :------: | :---: | :--: | :-: |
| $A_{1}A_{2}A_{3}A_{4}$ | $0$ | $CCCC$ | $D$ | $EEE$ | $FFF$ | $00000000$ |
| $A_{1}A_{2}A_{3}A_{4}$ | $1$ | $CCCC$ | $D$ | $EEE$ | $000$ | $GGGGGGGG$ |

#### Arithmetic Operation Instruction Code

- ADD
- SUB
- MUL
- DIV

| Flags | ImmArg | OpCode | EditFlag | Rdest | Rsrc | Imm |
| :---: | :----: | :----: | :------: | :---: | :--: | :-: |
| $A_{1}A_{2}A_{3}A_{4}$ | $0$ | $CCCC$ | $D$ | $EEE$ | $FFF$ | $GGGGGGGG$ |
| $A_{1}A_{2}A_{3}A_{4}$ | $1$ | $CCCC$ | $D$ | $EEE$ | $FFF$ | $GGGGGGGG$ |

