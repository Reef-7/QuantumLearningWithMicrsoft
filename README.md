# Quantum Programming with Microsoft Q# 🌌

A collection of quantum computing projects demonstrating fundamental quantum algorithms and concepts using Microsoft's Q# (Quantum Sharp) programming language. This repository serves as an educational resource for learning quantum computing through practical implementations and visualizations.

## 📚 Project Overview

This repository contains two main projects that explore different aspects of quantum computing:

1. **Quantum Phase & Inverse QFT Demo** - Demonstrates quantum state preparation, controlled phase rotations, and phase decoding using the Inverse Quantum Fourier Transform
2. **Simple Quantum Logic Circuit** - Explores the boundaries between quantum randomness and entanglement with a live Python visualization

## 🚀 Prerequisites

- **Azure Quantum Development Kit (QDK)** - Install the QDK extension for VS Code or the modern Q# compiler tools
- **Python 3.x** (for the visualization app)
- **Pygame** - For the quantum circuit visualization
- **qsharp** Python package - For integrating Q# with Python

### Installation

```bash
# Install Python dependencies
pip install pygame qsharp

# For Q#, install the Azure Quantum Development Kit extension in VS Code
# or follow the official Microsoft QDK installation guide
```

## 📁 Project Structure

```
Quantum Programming/
├── Demos/
│   ├── Demo1ReadMe.md          # Detailed explanation of the Phase & Inverse QFT demo
│   └── demo1.qs                # Q# implementation of quantum phase encoding
└── Simple_Quantum_Logic_Circuit/
    ├── Readme.md               # Explanation of randomness vs entanglement
    ├── example1.qs             # Q# quantum random circuit
    └── QuantumCircuitApp.py    # Python/Pygame visualization
```

---

## 🎯 Project 1: Quantum Phase & Inverse QFT Demo

### Overview
This beginner-friendly yet robust Q# project demonstrates quantum state preparation, controlled phase rotations, and phase decoding using the **Inverse Quantum Fourier Transform**. It showcases fundamental quantum computing algorithms implemented from scratch.

### What It Does
The program executes a complete quantum routine across 5 qubits:

1. **State Preparation** - Allocates 5 qubits (1 control, 4 target)
2. **Superposition & Phase Encoding** - Puts target qubits into superposition with unique, power-scaled phase shifts
3. **Controlled Operations** - Applies conditional `Rz` rotations controlled by the first qubit
4. **Phase Decoding (Inverse QFT)** - Runs a custom Inverse QFT to translate phases back into basis states
5. **State Inspection & Measurement** - Uses `DumpMachine()` for debugging and measures the qubits

### Key Functions

#### `ApplyInverseQFT(register : Qubit[]) : Unit`
A manual implementation of the Inverse Quantum Fourier Transform algorithm:
- Uses `SWAP` gates to reverse qubit order
- Applies controlled-phase rotations (`Controlled R1`)
- Uses Hadamard (`H`) gates for the QFT transformation

#### `CalculatePhaseWithPower(baseAngle : Double, power : Int) : Double`
Calculates phase angles by raising the base angle to a specified power, demonstrating non-linear phase progression.

#### `PrepareSuperpositionWithPhase(q : Qubit, baseAngle : Double, power : Int) : Unit`
Prepares a qubit in superposition state with a specific phase:
- Applies Hadamard gate for superposition
- Applies `Rz` rotation for phase encoding

#### `RunDemo1() : Result[]`
The main entry point that coordinates the entire execution flow from allocation to measurement.

### How to Run
1. Open the `Demos/demo1.qs` file in VS Code
2. Click the **"Run"** or **"Debug"** button above the `@EntryPoint()` macro
3. View the output in the debug console

### Sample Output
```text
Running demo with base angle 1.570795 and 3 iterations.
Calculated phase for base angle 1.570795 and power 3: 3.8757747638402096
Preparing superposition with phase on target qubits...
Applying controlled operations...
Applying Inverse QFT on target qubits to decode phases...

 Basis   | Amplitude      | Probability | Phase
 -------------------------------------------------
 |10010⟩ |  0.3978+0.1648𝑖 |    18.5428% |   0.3927
 |11010⟩ |  0.1820−0.4393𝑖 |    22.6131% |  -1.1781

Measuring qubits...
Measurement results: [Zero, Zero, Zero, One, One]
```

### Key Learning Points
- How to manipulate quantum phases using `Rz` and `R1` gates
- Manual implementation of the Inverse QFT circuit
- Managing qubit lifecycles with `use` blocks and `ResetAll`
- Using `DumpMachine()` for quantum state debugging

---

## 🎯 Project 2: Simple Quantum Logic Circuit

### Overview
A Q# implementation exploring the boundaries between **Pure Quantum Randomness** and **Quantum Entanglement**, complete with a live Python visualization using Pygame.

### The Quantum Mechanics
The circuit demonstrates a fascinating quantum paradox:

1. **Initialization**: Both qubits start at |00⟩
2. **First Hadamard (H(qA))**: Transforms to ½(|00⟩ + |10⟩)
3. **Second Hadamard (H(qB))**: Creates full superposition ½(|00⟩ + |01⟩ + |10⟩ + |11⟩)
4. **CNOT Gate**: Flips target qubit only if control is |1⟩

### The Paradox
After the CNOT, the state remains exactly the same due to perfect symmetry. The CNOT merely swaps state positions but creates **no entanglement** because the superposition was already symmetrical.

### Key Functions

#### `RunRandomCircuit() : (Result, Result)`
The main Q# operation that:
- Allocates two qubits
- Applies Hadamard gates to both
- Applies CNOT gate
- Measures both qubits
- Returns the measurement results

### Python Visualization (QuantumCircuitApp.py)
A Pygame-based live visualization showing:
- Real-time qubit movement through quantum gates
- Superposition state visualization (flickering 0/1)
- CNOT gate interaction animation
- Wave function collapse at measurement
- Integration with actual Q# circuit results

### How to Run the Visualization
```bash
cd Simple_Quantum_Logic_Circuit
python QuantumCircuitApp.py
```

Controls:
- **SPACE** - Run the simulation again after completion
- **Close window** - Exit the application

### Use Cases

#### 1. Quantum Random Number Generator (QRNG)
The circuit generates true quantum randomness with 25% probability for each outcome:
- (0, 0)
- (0, 1)
- (1, 0)
- (1, 1)

#### 2. Architectural Optimization Lesson
Demonstrates that not all quantum gates are necessary - the CNOT in this circuit is redundant since it doesn't change statistical outcomes. This teaches the importance of circuit optimization in real quantum computers where two-qubit gates are noisy and expensive.

### Creating True Entanglement (Bell State)
To convert this from a random generator to a true entangled state, **remove line 2** (`H(qB);`) from `example1.qs`. This creates a Bell State where outputs are strictly (0,0) or (1,1) with 50/50 probability, never mismatched.

---

## 🛠️ Technologies Used

- **Q# (Quantum Sharp)** - Microsoft's quantum programming language
- **Azure Quantum Development Kit** - Development tools for Q#
- **Python** - General-purpose programming language
- **Pygame** - Python library for creating visualizations and games
- **qsharp Python package** - Integration between Python and Q#

## 📖 Key Quantum Computing Concepts Demonstrated

- **Superposition** - Qubits existing in multiple states simultaneously
- **Entanglement** - Correlated quantum states
- **Quantum Gates** - H (Hadamard), CNOT, Rz, R1, SWAP
- **Quantum Fourier Transform (QFT)** - Fundamental quantum algorithm
- **Phase Encoding** - Storing information in quantum phases
- **Wave Function Collapse** - Measurement in quantum systems
- **Quantum Randomness** - True randomness from quantum mechanics

## 🎓 Learning Outcomes

This repository helps you understand:
- How to write quantum programs in Q#
- The difference between classical and quantum randomness
- How quantum gates transform quantum states
- The importance of circuit optimization
- How to visualize quantum operations
- Phase manipulation in quantum systems
- Implementation of quantum algorithms like QFT

## 📝 Notes

- The Phase & Inverse QFT demo intentionally uses non-linear phase progression (exponents instead of binary geometric progression), which causes "phase leakage" - a feature, not a bug, demonstrating quantum probability distribution
- The Simple Quantum Logic Circuit serves as both a QRNG and a lesson in quantum circuit optimization

## 🔗 Resources

- [Microsoft Q# Documentation](https://learn.microsoft.com/en-us/azure/quantum/)
- [Azure Quantum](https://azure.microsoft.com/en-us/products/quantum)
- [Quantum Computing Concepts](https://learn.microsoft.com/en-us/azure/quantum/concepts/)

---

*Created as part of a journey into Quantum Computing and Microsoft Q#*
