from influxdb import InfluxDBClient
from time import sleep
import psutil

client = InfluxDBClient(database="OTUS")


def get_cpu_load():
    cores = psutil.cpu_percent(percpu=True)
    data = {}
    for core, load in enumerate(cores):
        data[f'cpu{core}'] = load
    return data


def log_cpu_load():
    cpus = get_cpu_load()
    json_data = []
    for cpu, load in cpus.items():
        json_data.append({
            'measurement': 'cpu_usage',
            'tags': {
                'server': 'localhost',
                'cpu': cpu,
            },
            'fields': {
                'value': load,
            }
        })
    return client.write_points(json_data)


if __name__ == "__main__":
    while True:
        log_cpu_load()
        sleep(1)
