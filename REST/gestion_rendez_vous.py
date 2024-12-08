from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# Database setup
DATABASE_URL = "sqlite:///rendezvous.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Rendezvous(Base):
    __tablename__ = "rendezvous"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nom_patient = Column(String, nullable=False)
    date = Column(String, nullable=False)
    horaire = Column(String, nullable=False)

Base.metadata.create_all(engine)

@app.route('/', methods=['GET'])
def home():
    return "Bienvenue au service de gestion des rendez-vous !"

@app.route('/rendezvous', methods=['POST'])
def create_appointment():
    data = request.json
    appointment = Rendezvous(
        nom_patient=data['nom_patient'],
        date=data['date'],
        horaire=data['horaire']
    )
    session.add(appointment)
    session.commit()
    return jsonify({"id": appointment.id, "nom_patient": appointment.nom_patient, "date": appointment.date, "horaire": appointment.horaire}), 201

@app.route('/rendezvous', methods=['GET'])
def list_appointments():
    appointments = session.query(Rendezvous).all()
    return jsonify([{"id": a.id, "nom_patient": a.nom_patient, "date": a.date, "horaire": a.horaire} for a in appointments])

@app.route('/rendezvous/<int:id>', methods=['DELETE'])
def delete_appointment(id):
    appointment = session.query(Rendezvous).get(id)
    if appointment:
        session.delete(appointment)
        session.commit()
        return jsonify({"message": "Rendez-vous supprimé!"}), 200
    return jsonify({"error": "Rendez-vous non trouvé!"}), 404

if __name__ == '__main__':
    app.run(port=5000, debug=True)
