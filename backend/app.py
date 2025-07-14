from flask import Flask
from backend.routes.inventory_routes import inventory_bp  # Existing route (Feature 1)
from backend.routes.restocking import restocking_bp 
from backend.routes.eco_notifications import eco_bp# ✅ New route (Feature 2)
from backend.routes.vision_routes import vision_bp
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(inventory_bp, url_prefix='/api')
app.register_blueprint(restocking_bp, url_prefix='/api/restock')  # ✅ Predictive restocking
app.register_blueprint(eco_bp, url_prefix='/api')
app.register_blueprint(vision_bp)

if __name__ == '__main__':
    app.run(debug=True)
