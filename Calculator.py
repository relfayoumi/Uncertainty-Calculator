import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, convert_xor

def round_to_n_sig_figs(value, n=3):
    """
    Round a number to n total significant figures (including the first non-zero digit).
    Examples:
    - 61.51 -> 61.5 (3 total sig figs)
    - 2.41 -> 2.41 (3 total sig figs)
    - 0.0391 -> 0.0391 (3 total sig figs)
    - 0.0001234 -> 0.000123 (3 total sig figs)
    """
    if value == 0:
        return 0
    
    import math
    # Find the order of magnitude
    magnitude = math.floor(math.log10(abs(value)))
    # Round to n total significant figures
    # That's (magnitude - n + 1) decimal places
    decimal_places = magnitude - n + 1
    return round(value, -decimal_places)

def get_equation():
    print("Enter your equation (use ^ for powers):")
    raw_eq = input("> ").strip()
    # Define transformations to handle ^ as power
    transformations = standard_transformations + (convert_xor,)
    
    # Define constants to be recognized
    local_dict = {'pi': sympy.pi, 'e': sympy.E}
    
    try:
        # Parse the equation
        expr = parse_expr(raw_eq, local_dict=local_dict, transformations=transformations)
        return expr
    except Exception as e:
        print(f"Error parsing equation: {e}")
        return None

def get_user_inputs(variables):
    values = {}
    uncertainties = {}
    
    # Sort variables by name for consistent prompting
    sorted_vars = sorted(variables, key=lambda s: s.name)
    
    print(f"\nDetected variables: {', '.join([str(v) for v in sorted_vars])}")
    
    for var in sorted_vars:
        while True:
            try:
                val = float(input(f"Enter value for {var}: "))
                unc = float(input(f"Enter uncertainty for {var}: "))
                values[var] = val
                uncertainties[var] = unc
                break
            except ValueError:
                print("Invalid input. Please enter numeric values.")
                
    return values, uncertainties

def calculate_uncertainty(expr, values, uncertainties):
    # Calculate the value of the expression
    # subs returns a SymPy object (Float, Integer, etc.), convert to float for display
    calculated_value = float(expr.subs(values))
    
    variance = 0
    
    # Calculate propagated uncertainty
    # ΔQ = sqrt( sum( (dQ/dx_i * Δx_i)^2 ) )
    for var in values:
        # Partial derivative with respect to the variable
        partial_derivative = sympy.diff(expr, var)
        
        # Evaluate the partial derivative at the given values
        partial_val = float(partial_derivative.subs(values))
        
        sigma = uncertainties[var]
        
        term = (partial_val * sigma)**2
        variance += term
        
    absolute_uncertainty = variance**0.5
    
    return calculated_value, absolute_uncertainty

def values_only_mode():
    """Mode where user enters values and uncertainties directly without an equation."""
    print("\nValues-Only Mode")
    print("1) Addition/Subtraction")
    print("2) Multiplication/Division")
    
    while True:
        choice = input("Choose operation type (1 or 2): ").strip()
        if choice in {'1', '2'}:
            break
        print("Invalid choice. Please enter 1 or 2.")
    
    print("Enter your values (separated by spaces):")
    while True:
        try:
            values = [float(x) for x in input("> ").strip().split()]
            if not values:
                raise ValueError
            break
        except ValueError:
            print("Please enter valid numbers separated by spaces.")
    
    print(f"Enter the uncertainties for each value ({len(values)} values):")
    while True:
        try:
            uncertainties = [float(x) for x in input("> ").strip().split()]
            if len(uncertainties) != len(values):
                print(f"Expected {len(values)} uncertainties, got {len(uncertainties)}. Try again.")
                continue
            break
        except ValueError:
            print("Please enter valid numbers separated by spaces.")
    
    if choice == '1':
        # Addition/Subtraction
        val = sum(values)
        abs_unc = sum(uncertainties)
        operation_str = " + ".join(str(v) for v in values)
    else:
        # Multiplication/Division
        val = 1
        for v in values:
            val *= v
        
        # Relative uncertainties in quadrature
        rel_unc_sq = 0
        for v, u in zip(values, uncertainties):
            if v != 0:
                rel_unc_sq += (u / abs(v))**2
        rel_unc = rel_unc_sq**0.5
        abs_unc = abs(val) * rel_unc
        operation_str = " × ".join(str(v) for v in values)
    
    if val != 0:
        frac_unc = abs_unc / abs(val)
    else:
        frac_unc = 0.0
    
    # Round to 3 total significant figures
    val_rounded = round_to_n_sig_figs(val, n=3)
    abs_unc_rounded = round_to_n_sig_figs(abs_unc, n=3)
    frac_unc_rounded = round_to_n_sig_figs(frac_unc, n=3)
    
    print(f"\nOperation: {operation_str} = {val_rounded}")
    print(f"Computed value: {val_rounded}")
    print(f"Absolute uncertainty: {abs_unc_rounded}")
    print(f"Fractional uncertainty: {frac_unc_rounded}")

def main():
    print("Uncertainty Calculator")
    print("======================\n")
    
    while True:
        print("Main Menu:")
        print("1) Equation Mode (enter any equation)")
        print("2) Values-Only Mode (addition or multiplication)")
        
        while True:
            mode = input("Choose mode (1 or 2): ").strip()
            if mode in {'1', '2'}:
                break
            print("Invalid choice. Please enter 1 or 2.")
        
        if mode == '1':
            # Equation mode
            while True:
                expr = get_equation()
                if expr is None:
                    continue

                # Identify variables (free symbols)
                variables = expr.free_symbols
                
                if not variables:
                    # Case where equation is just constants, e.g. "pi * 2"
                    val = float(expr.evalf())
                    print(f"\nComputed value: {val}")
                    print("Absolute uncertainty: 0.0 (No variables)")
                    print("Fractional uncertainty: 0.0")
                else:
                    values, uncertainties = get_user_inputs(variables)
                    
                    try:
                        val, abs_unc = calculate_uncertainty(expr, values, uncertainties)
                        
                        if val != 0:
                            frac_unc = abs_unc / abs(val)
                        else:
                            frac_unc = 0.0
                        
                        # Round to 3 total significant figures
                        val_rounded = round_to_n_sig_figs(val, n=3)
                        abs_unc_rounded = round_to_n_sig_figs(abs_unc, n=3)
                        frac_unc_rounded = round_to_n_sig_figs(frac_unc, n=3)
                            
                        print(f"\nComputed value: {val_rounded}")
                        print(f"Absolute uncertainty: {abs_unc_rounded}")
                        print(f"Fractional uncertainty: {frac_unc_rounded}")
                        
                    except Exception as e:
                        print(f"An error occurred during calculation: {e}")
                
                # Ask if user wants another calculation in this mode
                while True:
                    choice = input("\nDo you want another calculation in this mode? (yes/no): ").strip().lower()
                    if choice in {'yes', 'y'}:
                        print("\n" + "="*40 + "\n")
                        break
                    elif choice in {'no', 'n'}:
                        break
                    else:
                        print("Please enter 'yes' or 'no'.")
                
                if choice in {'no', 'n'}:
                    break
        
        else:
            # Values-only mode
            values_only_mode()
        
        # Ask if user wants to return to main menu or exit
        while True:
            choice = input("\nReturn to main menu? (yes/no): ").strip().lower()
            if choice in {'yes', 'y'}:
                print("\n" + "="*40 + "\n")
                break
            elif choice in {'no', 'n'}:
                print("Thank you for using Uncertainty Calculator. Goodbye!")
                return
            else:
                print("Please enter 'yes' or 'no'.")

if __name__ == "__main__":
    main()
