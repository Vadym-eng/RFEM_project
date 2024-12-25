p = '''import math as mt

initial_value_section = int(input())
initial_value_force = abs(int(input()))
design_resistance = 23.5


def finding_optimization_value(section1, force, resistance):
    while stress <= resistance and difference <= 0.015:
        section = force / resistance
        difference = 1 - section / section1
        force = abs(int(input()))
        stress = force / section
        section1 = section
    return mt.sqrt(section)


required_value_side = finding_optimization_value(
    initial_value_section, initial_value_force, design_resistance
)'''


num1 = 76
forces1 = [0] * num1
#for i in range(1, num1 + 1):
#    forces1[i-1] = 1
print(forces1)