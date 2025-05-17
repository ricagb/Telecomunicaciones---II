from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost:3306",
    user="root",
    password="DAVIDpuentes3521..",
    database="sensor_data"
)

@app.route("/insertar_dato", methods=["POST"])
def insertar_dato():
    data = request.json
    print("Datos recibidos:", data)

    try:
        cursor = db.cursor()
        sql = "INSERT INTO sensores (nodo_id, tipo, valor, timestamp) VALUES (%s, %s, %s, %s)"
        # Asegúrate de que el timestamp sea formato DATETIME válido
        fecha = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        val = (data["id"], data["tipo"], float(data["valor"]), fecha)
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"status": "OK", "id": cursor.lastrowid})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
