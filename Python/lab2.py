import json
import logging
import os

# Налаштування логування
logging.basicConfig(filename='config_parser.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Декоратор для логування файлових операцій
def log_file_operations(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logging.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

class ConfigParser:
    def __init__(self):
        self.config = {}

    @log_file_operations
    def parse_config(self, file_path):
        """Парсить конфігураційний файл власного формату і створює словник з параметрами."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} does not exist")

        current_section = None
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, 1):
                line = line.strip()
                
                if not line or line.startswith('#'):
                    continue  # Пропускаємо пусті рядки та коментарі
                
                # Перевірка на секції [Section]
                if line.startswith('[') and line.endswith(']'):
                    current_section = line[1:-1].strip()
                    if current_section in self.config:
                        raise ValueError(f"Duplicate section '{current_section}' at line {line_num}")
                    self.config[current_section] = {}
                elif '=' in line:
                    if current_section is None:
                        raise ValueError(f"Key-value pair found outside of section at line {line_num}")
                    
                    key, value = map(str.strip, line.split('=', 1))
                    if key in self.config[current_section]:
                        raise ValueError(f"Duplicate key '{key}' in section '{current_section}' at line {line_num}")
                    self.config[current_section][key] = value
                else:
                    raise ValueError(f"Invalid line format at line {line_num}")
    
    def validate_config(self):
        """Валідація значень конфігурації."""
        if 'Database' in self.config:
            db_config = self.config['Database']
            if 'port' in db_config and not db_config['port'].isdigit():
                raise ValueError(f"Invalid port value in Database section: {db_config['port']}")
            logging.info("Database section validated successfully.")

        if 'API' in self.config:
            api_config = self.config['API']
            if 'timeout' in api_config and not api_config['timeout'].isdigit():
                raise ValueError(f"Invalid timeout value in API section: {api_config['timeout']}")
            logging.info("API section validated successfully.")
    
    @log_file_operations
    def save_to_json(self, json_file):
        """Зберігає конфігурацію у JSON файл."""
        with open(json_file, 'w') as file:
            json.dump(self.config, file, indent=4)
        logging.info(f"Configuration saved to {json_file}")
    
    @log_file_operations
    def load_from_json(self, json_file):
        """Завантажує конфігурацію з JSON файлу."""
        if not os.path.exists(json_file):
            raise FileNotFoundError(f"File {json_file} does not exist")
        
        with open(json_file, 'r') as file:
            self.config = json.load(file)
        logging.info(f"Configuration loaded from {json_file}")
    
    def get_config(self):
        """Повертає поточну конфігурацію."""
        return self.config


# Основна частина програми (перевірка на наявність файлу та його створення)
if __name__ == "__main__":
    # Перевірка наявності файлу config.txt
    if not os.path.exists('config.txt'):
        # Якщо файл відсутній, створюємо його з дефолтними налаштуваннями
        with open('config.txt', 'w') as f:
            f.write("[Database]\nhost=localhost\nport=5432\nuser=admin\npassword=secret\n")
            f.write("[API]\ntimeout=30\nbase_url=https://api.example.com\n")
        print("config.txt file was created with default settings.")

    # Створюємо екземпляр парсера
    parser = ConfigParser()

    # Парсинг конфігураційного файлу
    try:
        parser.parse_config('config.txt')
        parser.validate_config()

        # Збереження в JSON файл
        parser.save_to_json('config.json')

        # Завантаження з JSON файлу
        parser.load_from_json('config.json')
        print("Current config:", parser.get_config())

    except Exception as e:
        print(f"Error: {e}")

