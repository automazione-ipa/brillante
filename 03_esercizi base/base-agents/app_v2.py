from math_fib_agent import MathFibAgent
from temperature_agent import TemperatureAgent


def main():
    # Instanzia gli agenti
    math_agent = MathFibAgent()
    tmp_agent = TemperatureAgent()

    while True:
        # Menu di scelta
        print("\nScegli un'opzione:")
        print("1. Calcolare la sequenza di Fibonacci")
        print("2. Convertire la temperatura")
        print("3. Uscire")

        scelta = input("Inserisci il numero dell'opzione: ")

        if scelta == "1":
            # Calcolare la sequenza di Fibonacci
            n = int(input(
                "Inserisci il numero di termini per la sequenza di Fibonacci: "))
            print(f"Fibonacci Iterativo ({n} termini):",
                  math_agent.fibonacci_iterative(n))
            print(f"Fibonacci Ricorsivo ({n} termini):",
                  [MathFibAgent.fibonacci_recursive(i) for i in range(n)])

        elif scelta == "2":
            # Convertire la temperatura
            valore = float(
                input("Inserisci il valore della temperatura da convertire: "))
            from_unit = input(
                "Inserisci l'unità di partenza (kelvin, celsius, fahrenheit): ").lower()
            to_unit = input(
                "Inserisci l'unità di destinazione (kelvin, celsius, fahrenheit): ").lower()

            if from_unit not in ["kelvin", "celsius",
                                 "fahrenheit"] or to_unit not in ["kelvin",
                                                                  "celsius",
                                                                  "fahrenheit"]:
                print("Unità di temperatura non valide! Riprova.")
                continue

            # Esegui la conversione
            converted_value = tmp_agent.convert_temperature(value=valore,
                                                            from_unit=from_unit,
                                                            to_unit=to_unit)
            print(
                f"{valore} {from_unit.capitalize()} = {converted_value} {to_unit.capitalize()}")

        elif scelta == "3":
            print("Uscita... Arrivederci!")
            break  # Esce dal ciclo e termina l'applicazione

        else:
            print("Opzione non valida! Riprova.")


if __name__ == "__main__":
    main()
