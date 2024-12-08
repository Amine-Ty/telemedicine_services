from threading import Thread
from wsgiref.simple_server import make_server
from app.soap.medical_records_service import wsgi_app as medical_records_app
from app.soap.prescriptions_service import wsgi_app as prescriptions_app
from app.soap.doctors_service import wsgi_app as doctors_app
from app.database import init_db


def start_server(app, host, port):
    server = make_server(host, port, app)
    print(f"Service running on http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    init_db()
    print("Base de données recréée avec succès.")
    services = [
        (medical_records_app, '127.0.0.1', 8001),
        (prescriptions_app, '127.0.0.1', 8002),
        (doctors_app, '127.0.0.1', 8003),
    ]

    threads = []
    for app, host, port in services:
        thread = Thread(target=start_server, args=(app, host, port), daemon=True)
        threads.append(thread)
        thread.start()

    # Keep the main thread alive
    for thread in threads:
        thread.join()
