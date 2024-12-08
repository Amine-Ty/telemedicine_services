from sqlalchemy import Column, Integer, String, ForeignKey, Text, Date
from sqlalchemy.orm import relationship
from app.database import Base

# Modèle Patient avec plus d'informations
class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)  # Âge du patient
    gender = Column(String, nullable=True)  # Sexe du patient
    contact = Column(String, nullable=True)  # Informations de contact
    blood_type = Column(String, nullable=True)  # Groupe sanguin

    # Relation avec les dossiers médicaux
    medical_records = relationship("MedicalRecord", back_populates="patient")

# Modèle MedicalRecord avec plus d'informations sur le patient
class MedicalRecord(Base):
    __tablename__ = "medical_records"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    details = Column(Text, nullable=False)  # Détails supplémentaires sur le dossier médical
    allergies = Column(Text, nullable=True)  # Allergies du patient
    medical_history = Column(Text, nullable=True)  # Antécédents médicaux du patient
    medications = Column(Text, nullable=True)  # Médicaments en cours

    # Relation avec le modèle Patient
    patient = relationship("Patient", back_populates="medical_records")

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=True)

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    content = Column(Text, nullable=False)  # Contenu de la prescription
