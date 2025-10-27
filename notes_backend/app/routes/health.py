from flask_smorest import Blueprint
from flask.views import MethodView

# Root endpoint (keep for basic service info)
blp = Blueprint("Root", "root", url_prefix="/", description="Root endpoint")

@blp.route("")
class Root(MethodView):
    def get(self):
        return {"message": "Service running"}
