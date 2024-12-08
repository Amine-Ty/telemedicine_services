from spyne import Application, rpc, ServiceBase, Integer, Unicode, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from app.database import SessionLocal
from app.models import Doctor

class DoctorsService(ServiceBase):
    @rpc(Unicode, Unicode, _returns=Unicode)
    def add_doctor(ctx, name, specialty):
        session = SessionLocal()
        try:
            doctor = Doctor(name=name, specialty=specialty)
            session.add(doctor)
            session.commit()
            return f"Médecin ajouté avec l'ID {doctor.id}"
        finally:
            session.close()

    @rpc(Integer, Unicode, _returns=Unicode)
    def update_doctor(ctx, doctor_id, new_specialty):
        session = SessionLocal()
        try:
            doctor = session.query(Doctor).filter_by(id=doctor_id).first()
            if not doctor:
                raise Fault(f"Médecin avec ID {doctor_id} introuvable")
            doctor.specialty = new_specialty
            session.commit()
            return "Spécialité mise à jour"
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def delete_doctor(ctx, doctor_id):
        session = SessionLocal()
        try:
            doctor = session.query(Doctor).filter_by(id=doctor_id).first()
            if not doctor:
                raise Fault(f"Médecin avec ID {doctor_id} introuvable")
            session.delete(doctor)
            session.commit()
            return "Médecin supprimé"
        finally:
            session.close()

app = Application([DoctorsService], "telemedicine.soap.doctors", in_protocol=Soap11(validator="lxml"), out_protocol=Soap11())
wsgi_app = WsgiApplication(app)
