from spyne import Application, rpc, ServiceBase, Integer, Unicode, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from app.database import SessionLocal
from app.models import Patient, MedicalRecord

class MedicalRecordsService(ServiceBase):
    @rpc(Integer, Unicode, Unicode, Integer, Unicode, Unicode, Unicode, _returns=Unicode)  # Remplacer Date par Integer pour l'âge
    def create_medical_record(ctx, patient_id, name, details, age, gender, contact, blood_type):
        session = SessionLocal()
        try:
            # Chercher si le patient existe déjà, sinon créer un nouveau patient
            patient = session.query(Patient).filter_by(id=patient_id).first()
            if not patient:
                # Si le patient n'existe pas, créez un nouveau patient avec l'âge et autres informations
                patient = Patient(
                    id=patient_id,
                    name=name,  # Utilisation du paramètre 'name' pour le nom du patient
                    age=age,  # Utilisation de l'âge au lieu de la date de naissance
                    gender=gender,
                    contact=contact,
                    blood_type=blood_type
                )
                session.add(patient)
                session.commit()
                session.refresh(patient)  # Rafraîchir l'objet patient pour obtenir son ID

            # Créer le dossier médical
            record = MedicalRecord(
                patient_id=patient.id,
                details=details,
                allergies="None",  # Vous pouvez aussi accepter ces champs dans la requête si nécessaire
                medical_history="No medical history",
                medications="No medications"
            )
            session.add(record)
            session.commit()
            return f"Dossier médical créé pour le patient {patient.name} avec l'ID {record.id}"

        except Exception as e:
            session.rollback()
            raise Fault(f"Error: {str(e)}")
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def get_medical_record(ctx, record_id):
        session = SessionLocal()
        try:
            record = session.query(MedicalRecord).filter_by(id=record_id).first()
            if not record:
                raise Fault(f"Dossier médical avec ID {record_id} introuvable")
            return record.details
        finally:
            session.close()

    @rpc(Integer, Unicode, _returns=Unicode)
    def update_medical_record(ctx, record_id, new_details):
        session = SessionLocal()
        try:
            record = session.query(MedicalRecord).filter_by(id=record_id).first()
            if not record:
                raise Fault(f"Dossier médical avec ID {record_id} introuvable")
            record.details = new_details
            session.commit()
            return "Dossier médical mis à jour"
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def delete_medical_record(ctx, record_id):
        session = SessionLocal()
        try:
            record = session.query(MedicalRecord).filter_by(id=record_id).first()
            if not record:
                raise Fault(f"Dossier médical avec ID {record_id} introuvable")
            session.delete(record)
            session.commit()
            return "Dossier médical supprimé"
        finally:
            session.close()

# Création de l'application SOAP
app = Application([MedicalRecordsService], "telemedicine.soap.medical_records", in_protocol=Soap11(validator="lxml"), out_protocol=Soap11())
wsgi_app = WsgiApplication(app)
