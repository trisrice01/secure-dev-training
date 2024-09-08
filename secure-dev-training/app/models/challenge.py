import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.user_challenge_completions import UserChallengeCompletions
from app.models.user import User


class Challenge(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    ip_addr: so.Mapped[str] = so.mapped_column(sa.String)
    flag: so.Mapped[str] = so.mapped_column(sa.String)
    description: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    user_completions: so.Mapped[list[UserChallengeCompletions]] = so.relationship(back_populates="challenge")

    @property
    def completed_users(self):
        return list(uc.user for uc in self.user_completions)