from app.models.login_code import LoginCode
from sqlalchemy import desc

class LoginCodeService:
    def __init__(self, app, db):
        self.app = app
        self.db = db
    @staticmethod
    def init_app(app, db):
        return LoginCodeService(app, db)

    def set_login_code(self, login_code: str):
        new_login_code_item = LoginCode()
        new_login_code_item.login_code = login_code
        self.db.session.add(new_login_code_item)
        self.db.session.commit()

    def get_login_code(self):
        login_code = LoginCode.query.order_by(desc(LoginCode.id)).first()
        return None if not login_code else login_code.login_code

