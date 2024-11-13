from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from flask_login import UserMixin
from app.models.user_challenge_completions import UserChallengeCompletions
from app import db
import bcrypt


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    password: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    is_admin: so.Mapped[bool] = so.mapped_column(sa.Boolean, default=False)
    rdp_server: so.Mapped["RDPServer"] = so.relationship(back_populates="user")
    challenge_completions: so.Mapped[list["UserChallengeCompletions"]] = so.relationship(back_populates="user")
    question_completions: so.Mapped[list["UserMCQCompletions"]] = so.relationship(back_populates="user")
    # challenge_completions: so.Mapped[list["Challenge"]] = so.relationship(
    #     secondary=UserChallengeCompletions, back_populates="user_completions"
    # )

    def __repr__(self):
        return '<User {}>'.format(self.username)

    @property
    def rdp_server_connection(self):
        if self.is_admin:
            return None
        return self.rdp_server.ip_addr
        
    def verify_password(self, password_attempt):
        return bcrypt.checkpw(password_attempt.encode(), hashed_password=self.password)

    @property
    def completed_challenges(self):
        return list(cc.challenge for cc in self.challenge_completions)