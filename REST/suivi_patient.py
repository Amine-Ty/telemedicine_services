from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

DATABASE_URL = "sqlite:///patients.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    histories = relationship("History", back_populates="patient", cascade="all, delete-orphan")

class History(Base):
    __tablename__ = "histories"
    id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey('patients.id'))
    date = Column(String, nullable=False)
    report = Column(String, nullable=False)
    patient = relationship("Patient", back_populates="histories")

Base.metadata.create_all(engine)

@app.route('/patients', methods=['POST'])
def add_patient():
    data = request.json
    new_patient = Patient(name=data['name'])
    session.add(new_patient)
    session.commit()
    return jsonify({"id": new_patient.id, "name": new_patient.name}), 201

@app.route('/patients/<int:id>/history', methods=['POST'])
def add_history(id):
    data = request.json
    patient = session.query(Patient).get(id)
    if not patient:
        return jsonify({"error": "Patient non trouvé!"}), 404

    new_history = History(patient_id=patient.id, date=data['date'], report=data['report'])
    session.add(new_history)
    session.commit()
    return jsonify({"message": "Historique ajouté avec succès!"}), 201

@app.route('/patients/<int:id>', methods=['GET'])
def get_patient_history(id):
    patient = session.query(Patient).get(id)
    if not patient:
        return jsonify({"error": "Patient non trouvé!"}), 404

    return jsonify({
        "id": patient.id,
        "name": patient.name,
        "history": [{"date": h.date, "report": h.report} for h in patient.histories]
    })

if __name__ == '__main__':
    app.run(port=5002, debug=True)
