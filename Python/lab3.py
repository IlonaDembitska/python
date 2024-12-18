import time
import random
import logging
from functools import wraps

# Налаштування логування
logging.basicConfig(filename='sensor_log.log', level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# Генератори сенсорів
def temperature_sensor():
    """Генератор для симуляції температури."""
    while True:
        temp = round(random.uniform(-10, 40), 2)  # Випадкова температура від -10 до 40 градусів
        yield temp
        time.sleep(1)  # Імітуємо отримання даних кожну секунду

def pressure_sensor():
    """Генератор для симуляції тиску."""
    while True:
        pressure = round(random.uniform(950, 1050), 2)  # Випадковий тиск від 950 до 1050 hPa
        yield pressure
        time.sleep(1)

def humidity_sensor():
    """Генератор для симуляції вологості."""
    while True:
        humidity = round(random.uniform(0, 100), 2)  # Випадкова вологість від 0 до 100%
        yield humidity
        time.sleep(1)

# Декоратор для обробки сенсорних даних
def sensor_handler(sensor_type):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            data = args[0]
            logging.info(f"Sensor: {sensor_type}, Data: {data}")
            return func(self, *args, **kwargs)
        return wrapper
    return decorator

# Клас для обробки подій
class SensorSystem:
    
    def __init__(self):
        self.history = []

    @sensor_handler('Temperature')
    def handle_temperature(self, data):
        """Обробка температурних даних."""
        if data > 30:
            self.trigger_event(f"Warning! High temperature detected: {data} °C")
        self.history.append(('Temperature', data))

    @sensor_handler('Pressure')
    def handle_pressure(self, data):
        """Обробка даних тиску."""
        if data < 960:
            self.trigger_event(f"Warning! Low pressure detected: {data} hPa")
        self.history.append(('Pressure', data))

    @sensor_handler('Humidity')
    def handle_humidity(self, data):
        """Обробка даних вологості."""
        if data > 80:
            self.trigger_event(f"Warning! High humidity detected: {data}%")
        self.history.append(('Humidity', data))

    def trigger_event(self, message):
        """Реакція на подію."""
        logging.info(f"Event: {message}")
        print(message)

    def get_history(self):
        """Повертає історію отриманих даних."""
        return self.history


# Імітація роботи сенсорів та системи
if __name__ == "__main__":
    system = SensorSystem()

    temp_sensor = temperature_sensor()
    press_sensor = pressure_sensor()
    hum_sensor = humidity_sensor()

    try:
        while True:
            # Отримуємо дані від сенсорів
            temperature = next(temp_sensor)
            pressure = next(press_sensor)
            humidity = next(hum_sensor)

            # Обробляємо дані
            system.handle_temperature(temperature)
            system.handle_pressure(pressure)
            system.handle_humidity(humidity)

            time.sleep(1)  # Симуляція інтервалу між перевірками

    except KeyboardInterrupt:
        print("Система вимкнена.")
