# RISC-V Assembler & Simulator

## 📝 Project Overview

This repository contains a fully functional, custom-built **Assembler** and **Simulator** for a subset of the **RISC-V Instruction Set Architecture (ISA)**.

### The Assembler

The assembler parses RISC-V assembly language code, resolves labels, calculates PC-relative offsets, and translates instructions into **32-bit binary machine code**.

### The Simulator

The simulator reads the generated machine code and acts as a virtual CPU. It executes instructions cycle-by-cycle while maintaining the state of:

* Program Counter (PC)
* 32 General Purpose Registers
* Word-Aligned Memory Architecture

---

## ✨ Features

### Assembler Features

* Supports encoding of **R-Type, I-Type, S-Type, B-Type, and J-Type** instructions.
* Automatic **label resolution** using a two-pass assembly process.
* Correct computation of branch and jump offsets.
* Error detection for:

  * Invalid syntax
  * Unknown labels
  * Incorrect register names
  * Missing virtual halt instruction (`beq zero, zero, 0`)

### Simulator Features

* Decodes and executes machine code according to RISC-V specifications.
* Simulates all **32 registers (x0 – x31)**.
* Maintains **x0 as a hardwired zero register**.
* Generates a detailed execution trace after every instruction.
* Produces a final memory dump after program termination.

---

## 🛠️ Supported Instructions

### R-Type

* `add`
* `sub`
* `slt`
* `srl`
* `or`
* `and`

### I-Type

* `lw`
* `addi`
* `jalr`

### S-Type

* `sw`

### B-Type

* `beq`
* `bne`

### J-Type

* `jal`

---

## ⚙️ Setup & Usage

### 1. Running the Assembler (Automated Testing)

To run the assembler and evaluate it against all provided test cases, execute:

```powershell
powershell -ExecutionPolicy Bypass -File .\run_all_tests.ps1
```

The script:

* Compiles all assembly test files
* Compares generated binaries against expected outputs using Windows `fc`
* Displays a pass/fail summary
* Generates a `test_report.csv` file

---

### 2. Running the Simulator

#### Manual Execution

```bash
python3 Simulator.py <input_machine_code_file_path> <output_trace_file_path>
```

**Note:** Input and output files must use the `.txt` extension.

#### Automated Evaluation

Navigate to the `automatedTesting` directory and run:

##### Linux / macOS

```bash
python3 src/main.py --no-asm --linux
```

##### Windows

```bash
python3 src\main.py --no-asm --windows
```

---

## 📂 Project Components

### Assembler

Converts RISC-V assembly code into binary machine code by:

* Parsing instructions
* Resolving labels
* Computing branch/jump offsets
* Validating syntax

### Simulator

Executes machine code by:

* Decoding instructions
* Updating register values
* Managing memory operations
* Tracking PC progression
* Producing execution traces and memory dumps

---

## 👨‍💻 Contributors

* **Pratyaksh Kumar**
* **Sandeep Kumar**
* **Parth Verma**
* **Prateek Sharma**
