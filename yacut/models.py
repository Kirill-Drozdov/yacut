from datetime import datetime

from yacut import db
from yacut.constants import HOST_URL


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.Text, nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def to_dict(self):
        return dict(
            url=self.original,
            short_link=HOST_URL + self.short,
        )

    def from_dict(self, data):
        self.original = data.get('url')
        self.short = data.get('custom_id')
