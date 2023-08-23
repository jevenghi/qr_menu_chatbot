import qrcode
from .qr_repository import QRRepository
import io
from flask import make_response


class QRCode:
    @staticmethod
    def generate(qr_data):
        qr_model = QRRepository.create(qr_data)

        qr_id = qr_model.id
        qr_location_id = qr_model.location_id
        url = f"http://localhost:5000/location/{qr_location_id}"

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        qr_code_image = qr.make_image(fill_color="black", back_color="white")
        qr_code_image.save(f"qr_code{qr_id}.png")

        image_data = io.BytesIO()
        qr_code_image.save(image_data)
        image_data.seek(0)

        response = make_response(image_data.getvalue())
        response.headers.set("Content-Type", "image/png")
        response.headers.set(
            "Content-Disposition", "attachment", filename=f"qr_code{qr_id}.png"
        )

        return response
