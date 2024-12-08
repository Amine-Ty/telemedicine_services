from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

DATABASE_URL = "sqlite:///notifications.db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    message = Column(String, nullable=False)

Base.metadata.create_all(engine)

@app.route('/notifications', methods=['POST'])
def send_notification():
    data = request.json
    notification = Notification(
        type=data['type'],
        recipient=data['recipient'],
        message=data['message']
    )
    session.add(notification)
    session.commit()
    return jsonify({"message": "Notification envoyée", "details": {"id": notification.id, "type": notification.type, "recipient": notification.recipient, "message": notification.message}}), 201

@app.route('/notifications/history', methods=['GET'])
def notification_history():
    notifications = session.query(Notification).all()
    return jsonify([{"id": n.id, "type": n.type, "recipient": n.recipient, "message": n.message} for n in notifications])

if __name__ == '__main__':
    app.run(port=5001, debug=True)
