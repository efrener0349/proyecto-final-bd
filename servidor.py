from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import certifi
import os

app = Flask(__name__)
CORS(app)

# Tu enlace intacto
MONGO_URI = "mongodb+srv://efrener0349:jrxwZLg8EtCmrruc@efren.tr0fzs8.mongodb.net/?appName=efren"

# === EL PARCHE MAESTRO PARA EL ERROR SSL ===
ca = certifi.where()
client = MongoClient(MONGO_URI, tlsCAFile=ca)

db = client['organizacion_deportiva']
coleccion_jugadores = db['jugadores']

@app.route('/api/jugadores')
def obtener_jugadores():
    try:
        jugadores_lista = []
        # Intentamos buscar el roster en Mongo
        for jugador in coleccion_jugadores.find():
            jugadores_lista.append({
                "id": str(jugador["_id"]),
                "nombre": jugador.get("nombre", "Sin Nombre"),
                "posicion": jugador.get("posicion", "Sin Posición"),
                "numero": jugador.get("numero", 0)
            })
        return jsonify(jugadores_lista)
    except Exception as e:
        return jsonify({"error_tecnico": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
