from flask import Flask, request, jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.orm import scoped_session, sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
    engine = create_engine(DATABASE_URL.replace("postgres://", "postgresql://"))
    Session = scoped_session(sessionmaker(bind=engine))
else:
    engine = None
    Session = None

@app.route('/api/sensor', methods=['POST'])
def add_sensor_data():
    data = request.json
    temp = data.get('temperature')
    session = Session()
    session.execute(text("INSERT INTO sensor_data (temperature) VALUES (:temp)"), {'temp': temp})
    session.commit()
    return jsonify({'message': 'Podaci upisani'}), 201

@app.route('/api/sensor', methods=['GET'])
def get_sensor_data():
    session = Session()
    result = session.execute(text("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")).fetchall()
    data = [{'id': row[0], 'temperature': row[1], 'timestamp': row[2]} for row in result]
    return jsonify(data)

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': 'IoT Sensor API is running', 'endpoints': ['/api/sensor']})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5021)))
