import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from app.models.user_codechallenge_completions import UserCodeChallengeCompletions
from app.models.user import User


class CodeChallenge(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String, index=True)
    flag: so.Mapped[str] = so.mapped_column(sa.String)
    description: so.Mapped[str] = so.mapped_column(sa.String, nullable=True)
    vuln_code: so.Mapped[str] = so.mapped_column(sa.String)
    user_completions: so.Mapped[list[UserCodeChallengeCompletions]] = so.relationship(back_populates="challenge")

    @property
    def completed_users(self):
        return list(uc.user for uc in self.user_completions)
