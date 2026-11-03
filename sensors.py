import json
import random
import urllib.request
from typing import Protocol, runtime_checkable


@runtime_checkable
class TemperatureSensor(Protocol):
    def read_temperature(self) -> float:
        ...

    def get_sensor_id(self) -> str:
        ...


class WeatherAPISensor:
    def get_sensor_id(self) -> str:
        return "WAS26-Odesa"

    def read_temperature(self) -> float:
        url = "https://api.open-meteo.com/v1/forecast?latitude=46.48&longitude=30.73&current=temperature_2m"
        try:
            with urllib.request.urlopen(url, timeout=5) as resp:
                data = json.loads(resp.read())
            return data["current"]["temperature_2m"]
        except Exception as e:
            # якщо немає інтернету або апі не відповідає
            raise RuntimeError(f"Не вдалось отримати погоду ({e})")


class SimulatedSensor:
    def __init__(self, base: float, deviation: float):
        self.base = base
        self.deviation = deviation

    def get_sensor_id(self) -> str:
        return "SIM-1"

    def read_temperature(self) -> float:
        return self.base + random.uniform(-self.deviation, self.deviation)


class FakeAlways25:
    def get_sensor_id(self) -> str:
        return "Fake-25"

    def read_temperature(self) -> float:
        return 25.0


class BrokenSensor:
    def get_sensor_id(self) -> str:
        return "BROKEN-999"

    def read_temperature(self) -> float:
        raise RuntimeError("Датчик зламаний!")


# клас для перевірки isinstance, наслідування немає
class RealDHT22:
    def get_sensor_id(self) -> str:
        return "DHT22"

    def read_temperature(self) -> float:
        return 22.4


def monitor_room(sensors: list[TemperatureSensor]) -> None:
    for s in sensors:
        try:
            t = s.read_temperature()
            print(f"[{s.get_sensor_id()}] Температура: {t:.1f} °C")
        except Exception as e:
            print(f"[{s.get_sensor_id()}] ПОМИЛКА: {e}")


if __name__ == "__main__":
    sensors = [
        WeatherAPISensor(),
        SimulatedSensor(base=21.5, deviation=3.0),
        FakeAlways25(),
        BrokenSensor(),
    ]

    monitor_room(sensors)

    print()
    print(isinstance(RealDHT22(), TemperatureSensor))  # True
    print(isinstance({"temp": 22}, TemperatureSensor))  # False
