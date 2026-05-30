from flask import Flask, jsonify
from flask_cors import CORS
from pymongo import MongoClient
import os

app = Flask(__name__)
CORS(app)

# === REEMPLAZA CON TU ENLACE DE MONGODB ATLAS ===
MONGO_URI = "mongodb+srv://efrener0349:jrxwZLg8EtCmrruc@efren.tr0fzs8.mongodb.net/?appName=efren"
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['organizacion_deportiva']
coleccion_jugadores = db['jugadores']

@app.route('/api/jugadores')
def obtener_jugadores():
    try:
        jugadores_lista = []
        # Intentamos buscar en Mongo
        for jugador in coleccion_jugadores.find():
            jugadores_lista.append({
                "id": str(jugador["_id"]),
                "nombre": jugador.get("nombre", "Sin Nombre"),
                "posicion": jugador.get("posicion", "Sin Posición"),
                "numero": jugador.get("numero", 0)
            })
        return jsonify(jugadores_lista)
    except Exception as e:
        # Si algo falla, mostramos el error real en la pantalla
        return jsonify({"error_tecnico": str(e)}), 500

if __name__ == '__main__':
    # Render asigna el puerto automáticamente
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
