from .medical_records_service import wsgi_app as medical_records_app
from .prescriptions_service import wsgi_app as prescriptions_app
from .doctors_service import wsgi_app as doctors_app

__all__ = ["medical_records_app", "prescriptions_app", "doctors_app"]
