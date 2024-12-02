from machine import ADC

def initialize_adc(pin_number):
    """
    Initialize ADC for a given pin.
    """
    return ADC(pin_number)

def read_adc_value(adc, min_adc=0, max_adc=65535, min_coord=-300, max_coord=300):
    """
    Read ADC value and map it to a coordinate.
    """
    raw_value = adc.read_u16()
    mapped_value = min_coord + (raw_value - min_adc) * (max_coord - min_coord) / (max_adc - min_adc)
    return mapped_value

if __name__ == "__main__":
    x_pot = initialize_adc(26)  # Example ADC for X
    y_pot = initialize_adc(27)  # Example ADC for Y
    while True:
        x = read_adc_value(x_pot)
        y = read_adc_value(y_pot)
        print(f"X: {x}, Y: {y}")
