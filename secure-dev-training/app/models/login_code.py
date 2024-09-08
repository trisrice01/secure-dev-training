import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class LoginCode(db.Model):
    __tablename__ = "login_code"

    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    login_code: so.Mapped[str] = so.mapped_column(sa.String)