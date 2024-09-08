import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class UserChallengeCompletions(db.Model):
    __tablename__ = "user_challenge_completions"

    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    challenge_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('challenge.id'), primary_key=True)

    user: so.Mapped["User"] = so.relationship(back_populates="challenge_completions")
    challenge: so.Mapped["Challenge"] = so.relationship(back_populates="user_completions")