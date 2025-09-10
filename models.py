from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Advertiser(db.Model):
    __tablename__ = "advertisers"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    domain = db.Column(db.String)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class TrackedSite(db.Model):
    __tablename__ = "tracked_sites"
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'))
    url = db.Column(db.Text, nullable=False)
    css_selector = db.Column(db.Text)
    active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdRecord(db.Model):
    __tablename__ = "ads"
    id = db.Column(db.Integer, primary_key=True)
    advertiser_id = db.Column(db.Integer, db.ForeignKey('advertisers.id'))
    tracked_site_id = db.Column(db.Integer, db.ForeignKey('tracked_sites.id'))
    ad_hash = db.Column(db.String, nullable=False, index=True)
    title = db.Column(db.Text)
    body = db.Column(db.Text)
    landing_url = db.Column(db.Text)
    creative_path = db.Column(db.Text)
    detected_at = db.Column(db.DateTime, default=datetime.utcnow)
    first_seen = db.Column(db.DateTime)
    last_seen = db.Column(db.DateTime)
    status = db.Column(db.String, default='active')