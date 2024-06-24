from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app import db
import bcrypt


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    rdp_server: so.Mapped["RDPServer"] = so.relationship(back_populates="user")

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def rdp_server_connection(self):
        return self.rdp_server.ip_addr
        
    def verify_password(self, password_attempt):
        return bcrypt.checkpw(password_attempt.encode(), hashed_password=self.password)
    