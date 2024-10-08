from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'GET':
        return [message.to_dict() for message in Message.query.all()]
    elif request.method == 'POST':
        json_body = request.json
        new_message = Message(username=json_body['username'],
                              body=json_body['body'])
        db.session.add(new_message)
        db.session.commit()
        return new_message.to_dict(), 201


@app.route('/messages/<int:message_id>', methods=['PATCH', 'DELETE'])
def message_by_id(message_id):
    message = Message.query.get(message_id)

    if request.method == 'PATCH':
        for key, value in request.json.items():
            setattr(message, key, value)
        db.session.commit()
        return message.to_dict()

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        return jsonify(message='Successfully deleted resource.')


if __name__ == '__main__':
    app.run(port=5555)
