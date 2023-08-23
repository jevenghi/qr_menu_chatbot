from sqlalchemy.exc import SQLAlchemyError, IntegrityError, ProgrammingError, DataError
from flask import jsonify
from flask_smorest import abort
from ..db import db
from ..tag import ItemTags, TagModel

def create_model(model, data):
    tag_ids = data.pop('tags', [])
    model_data = model(**data)

    try:
        db.session.add(model_data)
        db.session.flush()

        for tag_data in tag_ids:
            tag_id = tag_data['id']
            item_tag = ItemTags(item_id=model_data.id, tag_id=tag_id)
            db.session.add(item_tag)

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