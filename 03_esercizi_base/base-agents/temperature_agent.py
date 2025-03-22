class TemperatureAgent:
    def __init__(self):
        pass

    @staticmethod
    def convert(value, factor, offset=0.0):
        """Funzione generica di conversione"""
        return value * factor + offset

    def kelvin_to_celsius(self, kelvin):
        """Converte la temperatura da Kelvin a Celsius"""
        return self.convert(kelvin, 1, -273.15)

    def kelvin_to_fahrenheit(self, kelvin):
        """Converte la temperatura da Kelvin a Fahrenheit"""
        return self.convert(kelvin, 9 / 5, -459.67)

    def celsius_to_kelvin(self, celsius):
        """Converte la temperatura da Celsius a Kelvin"""
        return self.convert(celsius, 1, 273.15)

    def celsius_to_fahrenheit(self, celsius):
        """Converte la temperatura da Celsius a Fahrenheit"""
        return self.convert(celsius, 9 / 5, 32)

    def fahrenheit_to_kelvin(self, fahrenheit):
        """Converte la temperatura da Fahrenheit a Kelvin"""
        return self.convert(fahrenheit, 5 / 9, 255.372)

    def fahrenheit_to_celsius(self, fahrenheit):
        """Converte la temperatura da Fahrenheit a Celsius"""
        return self.convert(fahrenheit, 5 / 9, -32)

    def convert_temperature(self, value, from_unit, to_unit):
        """Converte la temperatura da una unità di misura a un'altra"""
        conversion_map = {
            ("kelvin", "celsius"): self.kelvin_to_celsius,
            ("kelvin", "fahrenheit"): self.kelvin_to_fahrenheit,
            ("celsius", "kelvin"): self.celsius_to_kelvin,
            ("celsius", "fahrenheit"): self.celsius_to_fahrenheit,
            ("fahrenheit", "kelvin"): self.fahrenheit_to_kelvin,
            ("fahrenheit", "celsius"): self.fahrenheit_to_celsius
        }

        # Controlla se la coppia di unità è valida
        if (from_unit, to_unit) not in conversion_map:
            raise ValueError(
                f"Conversione non supportata tra {from_unit} e {to_unit}")

        # Richiama la funzione di conversione corretta
        convert_func = conversion_map[(from_unit, to_unit)]
        return convert_func(value)

