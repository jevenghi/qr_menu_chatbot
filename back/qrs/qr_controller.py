import qrcode
from .qr_repository import PlainQRSchema
import io
from flask import make_response
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from .qr_service import QRCode

blp = Blueprint("qrs", __name__, description="Operations on qrs")


@blp.route("/qr")
class QR(MethodView):
    @blp.arguments(PlainQRSchema)
    def post(self, qr_data):
        qr = QRCode.generate(qr_data)
        return qr
