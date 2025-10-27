from flask_smorest import Blueprint
from flask.views import MethodView


blp = Blueprint("Health", "health", url_prefix="/health", description="Health check endpoint")

@blp.route("")
class Health(MethodView):
    # PUBLIC_INTERFACE
    def get(self):
        """Return simple health status for liveness/readiness checks."""
        return {"status": "ok"}
