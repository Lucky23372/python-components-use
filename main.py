import psutil
import time
import csv
from datetime import datetime
from threading import Thread
import speedtest
from flask import Flask, render_template, jsonify

# Inicjalizacja aplikacji Flask
app = Flask(__name__)

# Lista do przechowywania danych
data_points = []

# Funkcja monitorująca zużycie CPU, RAM i internetu
def monitor_and_save():
    while True:
        # Pobierz bieżące wartości
        cpu_percent = psutil.cpu_percent()
        ram_percent = psutil.virtual_memory().percent

        # Speedtest
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = st.download() / 1e6  # Mbps
        upload_speed = st.upload() / 1e6  # Mbps

        # Zapisz czas pomiaru
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Zapisz dane
        data_points.append({
            'timestamp': timestamp,
            'cpu_percent': cpu_percent,
            'ram_percent': ram_percent,
            'download_speed': download_speed,
            'upload_speed': upload_speed
        })

        # Poczekaj 1 sekundę przed kolejnym pomiarem
        time.sleep(1)

# Wątek do monitorowania
monitor_thread = Thread(target=monitor_and_save)
monitor_thread.start()

# Endpoint do zwracania danych w formacie JSON
@app.route('/data', methods=['GET'])
def get_data():
    return jsonify(data_points)

# Endpoint do renderowania strony z wykresami
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Endpoint do wykonania speedtestu
@app.route('/speedtest', methods=['POST'])
def run_speedtest():
    st = speedtest.Speedtest()
    st.get_best_server()
    st.download()
    st.upload()
    return jsonify({'message': 'Speedtest completed.'})

# Uruchomienie aplikacji Flask na porcie 2000
if __name__ == '__main__':
    app.run(port=2000)
