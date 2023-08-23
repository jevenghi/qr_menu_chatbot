from sqlalchemy.exc import SQLAlchemyError, IntegrityError, ProgrammingError, DataError
from flask import jsonify
from flask_smorest import abort
from .db import db

def create_model(model, data):
    model_data = model(**data)
    try:
        db.session.add(model_data)
        db.session.commit()
    except IntegrityError as error:
        db.session.rollback()
        error_message = str(error.orig)
        return jsonify(message="An integrity error occurred", error=error_message), 500
    except ProgrammingError as error:
        db.session.rollback()
        error_message = str(error.orig)
        return jsonify(message="A programming error occurred", error=error_message), 500
    except DataError as error:
        db.session.rollback()
        error_message = str(error.orig)
        return jsonify(message="A Data error occurred", error=error_message), 500
    except SQLAlchemyError as error:
        abort(500, message=error)
    return model_data
