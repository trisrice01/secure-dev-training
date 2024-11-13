from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Module(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    path: so.Mapped[str] = so.mapped_column(sa.String(64))
    constant: so.Mapped[str] = so.mapped_column(sa.String(64), default="aaa")
    is_enabled: so.Mapped[bool] = so.mapped_column(sa.Boolean)
