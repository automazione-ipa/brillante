from math_fib_agent import MathFibAgent
from temperature_agent import TemperatureAgent
math_agent = MathFibAgent()

print(
    "Iterative Fibonacci:",
    math_agent.fibonacci_iterative(10)
)

print(
    "Recursive Fibonacci:",
    [MathFibAgent.fibonacci_recursive(i) for i in range(10)]
)


# Creazione di un'istanza dell'agente
tmp_agent = TemperatureAgent()
KELVIN = "kelvin"
CELSIUS = "celsius"
FAHRENHEIT = "fahrenheit"
# Esempio di utilizzo
kelvin_value = tmp_agent.convert_temperature(
    value=35, from_unit=CELSIUS, to_unit=FAHRENHEIT
)
print(f"12 °C = {kelvin_value} K")
