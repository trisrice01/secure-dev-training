import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db


class UserCodeChallengeCompletions(db.Model):
    __tablename__ = "user_codechallenge_completions"

    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    challenge_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('code_challenge.id'), primary_key=True)

    user: so.Mapped["User"] = so.relationship(back_populates="codechallenge_completions")
    challenge: so.Mapped["CodeChallenge"] = so.relationship(back_populates="user_completions")
