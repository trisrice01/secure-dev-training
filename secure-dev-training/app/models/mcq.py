from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

class Question(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    question_text: so.Mapped[str] = so.mapped_column(sa.String(64))
    order: so.Mapped[int] = so.mapped_column(sa.Integer()   , autoincrement=True) 
    question_choices: so.Mapped[list["QuestionChoice"]] = so.relationship(back_populates="question")
    user_completions: so.Mapped[list["UserMCQCompletions"]] = so.relationship(back_populates="question", cascade="all, delete-orphan")

    @property
    def is_multi_choice(self):
        return len(list(filter(lambda x: x.is_correct, self.question_choices))) > 1
    
    def to_response(self):
        return {
            "question_id": self.id,
            "question": self.question_text,
            "is_multi_choice": self.is_multi_choice,
            "choices": [
                {
                    "id": choice.id,
                    "choice_text": choice.choice_text
                }
                for choice in self.question_choices
            ]
        }

@sa.event.listens_for(Question, 'before_insert')
def receive_before_insert(mapper, connection, target):
    if target.order is None:
        max_new_id = connection.execute(db.select(db.func.max(Question.order))).scalar() or 0
        target.order = max_new_id + 1



class QuestionChoice(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    choice_text: so.Mapped[str] = so.mapped_column(sa.String(64))
    is_correct: so.Mapped[bool] = so.mapped_column(sa.Boolean)
    question_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey("question.id"), nullable=True)
    question: so.Mapped["Question"] = so.relationship(back_populates="question_choices")

class UserMCQCompletions(db.Model):
    __tablename__ = "user_mcq_completions"

    user_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('user.id'), primary_key=True)
    question_id: so.Mapped[int] = so.mapped_column(sa.Integer, sa.ForeignKey('question.id', ondelete="CASCADE"), primary_key=True)

    user: so.Mapped["User"] = so.relationship(back_populates="question_completions")
    question: so.Mapped["Question"] = so.relationship(back_populates="user_completions")