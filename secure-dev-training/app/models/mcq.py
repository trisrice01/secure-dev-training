from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Question(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question_text: so.Mapped[str] = so.mapped_column(sa.String(64))
    questions = 


class QuestionChoice(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    choice_text: so.Mapped[str] = so.mapped_column(sa.String(64))
    is_correct: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    question_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("question.id"), nullable=True)
    question: so.Mapped["Question"] = so.relationship(back_populates="question_choice")