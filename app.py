from flask import Flask, jsonify, request
from models import db, AdRecord
from config import DATABASE_URL

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify({"status":"ok"})

    @app.route("/ads", methods=["GET"])
    def list_ads():
        q = AdRecord.query.order_by(AdRecord.detected_at.desc()).limit(200).all()
        return jsonify([{
            "id": a.id, "title": a.title, "body": a.body,
            "landing_url": a.landing_url, "creative": a.creative_path,
            "detected_at": a.detected_at.isoformat()
        } for a in q])

    @app.route("/ads", methods=["POST"])
    def ingest_ad():
        data = request.json
        ad = AdRecord(
            advertiser_id=data.get("advertiser_id"),
            tracked_site_id=data.get("tracked_site_id"),
            ad_hash=data["ad_hash"],
            title=data.get("title"),
            body=data.get("body"),
            landing_url=data.get("landing_url"),
            creative_path=data.get("creative_path")
        )
        db.session.add(ad)
        db.session.commit()
        return jsonify({"status":"ok", "id": ad.id}), 201

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)