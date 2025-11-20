# Uncertainty Calculator

A Python-based uncertainty calculator that performs error propagation for mathematical equations and simple operations. This tool helps scientists, engineers, and students calculate how uncertainties in measured values propagate through calculations.

## Table of Contents
- [Overview](#overview)
- [Theory: Uncertainty Propagation](#theory-uncertainty-propagation)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Code Implementation](#code-implementation)
- [Examples](#examples)

## Overview

The Uncertainty Calculator provides two modes of operation:
1. **Equation Mode**: Enter any mathematical equation with variables, and the calculator computes the propagated uncertainty using partial derivatives.
2. **Values-Only Mode**: Quick calculations for addition/subtraction or multiplication/division operations.

## Theory: Uncertainty Propagation

### General Formula for Error Propagation

For a function Q that depends on multiple variables x₁, x₂, ..., xₙ:

```
Q = f(x₁, x₂, ..., xₙ)
```

The absolute uncertainty ΔQ is calculated using the **propagation of uncertainty formula**:

```
ΔQ = √[Σᵢ (∂Q/∂xᵢ · Δxᵢ)²]
```

Where:
- `∂Q/∂xᵢ` is the partial derivative of Q with respect to variable xᵢ
- `Δxᵢ` is the uncertainty in variable xᵢ
- The sum is taken over all independent variables

### Fractional (Relative) Uncertainty

The fractional uncertainty is defined as:

```
Fractional Uncertainty = ΔQ / |Q|
```

### Special Cases

#### Addition and Subtraction
For Q = a ± b ± c ± ...:

```
ΔQ = √[(Δa)² + (Δb)² + (Δc)² + ...]
```

For uncorrelated uncertainties, this simplifies to direct addition when all terms have the same sign:
```
ΔQ ≈ Δa + Δb + Δc + ... (when Δ values are similar in magnitude)
```

#### Multiplication and Division
For Q = a × b × c × ... or Q = a / b / c / ...:

```
(ΔQ/Q)² = (Δa/a)² + (Δb/b)² + (Δc/c)² + ...
```

Therefore:
```
ΔQ = |Q| × √[(Δa/a)² + (Δb/b)² + (Δc/c)² + ...]
```

#### Powers
For Q = xⁿ:

```
ΔQ/|Q| = |n| × (Δx/|x|)
```

## Features

- **Equation Mode**: 
  - Parse and evaluate any mathematical expression
  - Automatic detection of variables
  - Symbolic differentiation for uncertainty calculation
  - Support for common mathematical functions and constants (π, e)
  - Use `^` for exponentiation

- **Values-Only Mode**:
  - Quick calculations for addition/subtraction
  - Quick calculations for multiplication/division
  - No need to write equations

- **Output**:
  - Computed value rounded to 3 significant figures
  - Absolute uncertainty (ΔQ)
  - Fractional/relative uncertainty (ΔQ/Q)

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Install Dependencies

```bash
pip install sympy
```

### Download and Run

```bash
# Clone or download the repository
git clone https://github.com/relfayoumi/Uncertainty-Calculator.git
cd Uncertainty-Calculator

# Run the calculator
python Calculator.py
```

## Usage

### Starting the Calculator

Run the calculator:
```bash
python Calculator.py
```

You'll see the main menu:
```
Uncertainty Calculator
======================

Main Menu:
1) Equation Mode (enter any equation)
2) Values-Only Mode (addition or multiplication)
Choose mode (1 or 2):
```

### Equation Mode

1. Select option `1` from the main menu
2. Enter your equation using standard mathematical notation
   - Use `^` for powers (e.g., `x^2` for x²)
   - Use standard operators: `+`, `-`, `*`, `/`
   - Use parentheses for grouping: `(a + b) * c`
   - Access constants: `pi`, `e`
   - Use functions: `sqrt()`, `sin()`, `cos()`, `log()`, etc.

3. The calculator will identify all variables
4. Enter the value and uncertainty for each variable
5. View the computed result with uncertainties

### Values-Only Mode

1. Select option `2` from the main menu
2. Choose operation type:
   - `1` for Addition/Subtraction
   - `2` for Multiplication/Division
3. Enter values separated by spaces
4. Enter uncertainties (same number as values) separated by spaces
5. View the computed result with uncertainties

## Code Implementation

### Key Components

#### 1. Expression Parsing (`get_equation`)
Uses SymPy's `parse_expr` to convert string input into symbolic mathematical expressions:

```python
expr = parse_expr(raw_eq, local_dict=local_dict, transformations=transformations)
```

This allows the calculator to:
- Recognize mathematical operators and functions
- Identify variables automatically
- Support symbolic mathematics

#### 2. Uncertainty Calculation (`calculate_uncertainty`)

Implements the general uncertainty propagation formula:

```python
variance = 0
for var in values:
    # Calculate ∂Q/∂xᵢ
    partial_derivative = sympy.diff(expr, var)
    
    # Evaluate at given values
    partial_val = float(partial_derivative.subs(values))
    
    # Add (∂Q/∂xᵢ · Δxᵢ)² to variance
    sigma = uncertainties[var]
    term = (partial_val * sigma)**2
    variance += term

# ΔQ = √(variance)
absolute_uncertainty = variance**0.5
```

**Mathematical Explanation:**
- `sympy.diff(expr, var)` computes the partial derivative ∂Q/∂xᵢ symbolically
- `.subs(values)` evaluates the partial derivative at the given point
- The sum of squared terms follows the propagation formula
- Taking the square root gives the absolute uncertainty

#### 3. Significant Figures (`round_to_n_sig_figs`)

Rounds results to n significant figures (default: 3):

```python
magnitude = math.floor(math.log10(abs(value)))
decimal_places = magnitude - n + 1
return round(value, -decimal_places)
```

This ensures results are presented with appropriate precision.

#### 4. Values-Only Mode (`values_only_mode`)

Implements simplified formulas:

**Addition/Subtraction:**
```python
val = sum(values)
abs_unc = sum(uncertainties)  # Direct sum for linear operations
```

**Multiplication/Division:**
```python
val = product(values)
# Calculate relative uncertainties in quadrature
rel_unc_sq = sum((u/v)² for v, u in zip(values, uncertainties))
rel_unc = √(rel_unc_sq)
abs_unc = |val| × rel_unc
```

### Data Flow

1. **Input** → Parse equation or values
2. **Analysis** → Identify variables, compute derivatives
3. **Calculation** → Apply uncertainty propagation formulas
4. **Output** → Round and display results

## Examples

### Example 1: Multiplication (Equation Mode)

**Problem:** Calculate the area of a rectangle: A = length × width

**Input:**
```
Choose mode: 1
Enter equation: l * w
Enter value for l: 5.0
Enter uncertainty for l: 0.1
Enter value for w: 3.0
Enter uncertainty for w: 0.15
```

**Output:**
```
Computed value: 15.0
Absolute uncertainty: 0.808
Fractional uncertainty: 0.0539
```

**Calculation Explanation:**
- Q = l × w = 5.0 × 3.0 = 15.0
- ∂Q/∂l = w = 3.0
- ∂Q/∂w = l = 5.0
- ΔQ = √[(∂Q/∂l · Δl)² + (∂Q/∂w · Δw)²]
- ΔQ = √[(3.0 × 0.1)² + (5.0 × 0.15)²]
- ΔQ = √[0.09 + 0.5625] = √0.6525 ≈ 0.808

### Example 2: Power Function (Equation Mode)

**Problem:** Calculate kinetic energy: KE = ½mv²

**Input:**
```
Choose mode: 1
Enter equation: 0.5 * m * v^2
Enter value for m: 2.0
Enter uncertainty for m: 0.1
Enter value for v: 10.0
Enter uncertainty for v: 0.5
```

**Output:**
```
Computed value: 100.0
Absolute uncertainty: 11.2
Fractional uncertainty: 0.112
```

**Calculation Explanation:**
- Q = 0.5 × m × v² = 0.5 × 2.0 × 100 = 100.0
- ∂Q/∂m = 0.5 × v² = 0.5 × 100 = 50
- ∂Q/∂v = m × v = 2.0 × 10.0 = 20
- ΔQ = √[(50 × 0.1)² + (20 × 0.5)²]
- ΔQ = √[25 + 100] = √125 ≈ 11.2

### Example 3: Addition (Values-Only Mode)

**Problem:** Sum three measurements: 5.0 ± 0.2, 10.5 ± 0.3, 3.2 ± 0.1

**Input:**
```
Choose mode: 2
Choose operation: 1
Enter values: 5.0 10.5 3.2
Enter uncertainties: 0.2 0.3 0.1
```

**Output:**
```
Operation: 5.0 + 10.5 + 3.2 = 18.7
Computed value: 18.7
Absolute uncertainty: 0.6
Fractional uncertainty: 0.0321
```

**Calculation Explanation:**
- Q = 5.0 + 10.5 + 3.2 = 18.7
- ΔQ = 0.2 + 0.3 + 0.1 = 0.6

### Example 4: Division (Values-Only Mode)

**Problem:** Calculate density: ρ = m/V = 100g / 50cm³

**Input:**
```
Choose mode: 2
Choose operation: 2
Enter values: 100 0.02  (entering 100 then 1/50 = 0.02)
Enter uncertainties: 2 0.001
```

For division by 50 with uncertainty:
```
Enter values: 100 50
Enter uncertainties: 2 1
```

**Output (for 100/50):**
```
Computed value: 2.0
Absolute uncertainty: 0.0458
Fractional uncertainty: 0.0229
```

**Calculation Explanation:**
- Q = 100/50 = 2.0
- (ΔQ/Q)² = (2/100)² + (1/50)² = 0.0004 + 0.0004 = 0.0008
- ΔQ/Q = √0.0008 ≈ 0.0283
- ΔQ = 2.0 × 0.0283 ≈ 0.0566

### Example 5: Complex Equation

**Problem:** Projectile range formula: R = (v²sin(2θ))/g

**Input:**
```
Choose mode: 1
Enter equation: (v^2 * sin(2*theta)) / g
Enter value for g: 9.8
Enter uncertainty for g: 0.1
Enter value for theta: 0.785  (45° in radians)
Enter uncertainty for theta: 0.01
Enter value for v: 20
Enter uncertainty for v: 0.5
```

The calculator will:
1. Parse the equation
2. Compute partial derivatives for v, theta, and g
3. Evaluate derivatives at given values
4. Calculate propagated uncertainty
5. Display results with 3 significant figures

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve this calculator.

## License

This project is open source and available for educational and scientific use.

## Author

Created by relfayoumi
