from spyne import Application, rpc, ServiceBase, Integer, Unicode, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from app.database import SessionLocal
from app.models import Prescription

class PrescriptionsService(ServiceBase):
    @rpc(Integer, Integer, Unicode, _returns=Unicode)
    def add_prescription(ctx, patient_id, doctor_id, content):
        session = SessionLocal()
        try:
            prescription = Prescription(patient_id=patient_id, doctor_id=doctor_id, content=content)
            session.add(prescription)
            session.commit()
            return f"Prescription créée avec l'ID {prescription.id}"
        except Exception as e:
            session.rollback()
            raise Fault(f"Error: {str(e)}")
        finally:
            session.close()

    @rpc(Integer, _returns=Unicode)
    def get_prescriptions(ctx, patient_id):
        session = SessionLocal()
        try:
            prescriptions = session.query(Prescription).filter_by(patient_id=patient_id).all()
            return "\n".join([f"ID: {p.id}, Content: {p.content}" for p in prescriptions])
        finally:
            session.close()

app = Application([PrescriptionsService], "telemedicine.soap.prescriptions", in_protocol=Soap11(validator="lxml"), out_protocol=Soap11())
wsgi_app = WsgiApplication(app)
