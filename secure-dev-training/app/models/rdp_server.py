import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.user import User

class RDPServer(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    ip_addr: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    is_taken: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False, nullable=True)
    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("user.id"), nullable=True)
    user: so.Mapped["User"] = so.relationship(back_populates="rdp_server")

    def __repr__(self):
        return '<RDP Server {}>'.format(self.ip_addr)
