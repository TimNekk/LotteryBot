from tgbot.models.db import TimedBaseModel, db


class User(TimedBaseModel):
    __tablename__ = "users"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    username = db.Column(db.String(32), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    is_banned = db.Column(db.Boolean, nullable=False, server_default="False")
    deep_link = db.Column(db.String(225), nullable=True)
    attempts = db.Column(db.Integer, nullable=False, server_default="0")
    has_won = db.Column(db.Boolean, nullable=False, server_default="False")
