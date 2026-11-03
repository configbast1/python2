# Протокол TemperatureSensor

Протокол `TemperatureSensor` (`typing.Protocol` + `@runtime_checkable`) і чотири датчики:

- `WeatherAPISensor` — поточна температура в Одесі з open-meteo.com
- `SimulatedSensor` — базова температура + випадкове відхилення
- `FakeAlways25` — завжди 25.0 °C
- `BrokenSensor` — завжди піднімає `RuntimeError("Датчик зламаний!")`

Функція `monitor_room()` виводить температуру кожного датчика або помилку.

## Запуск

```
python sensors.py
```
