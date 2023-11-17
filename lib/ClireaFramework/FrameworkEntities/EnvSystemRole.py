from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .ClireaBase import ClireaBase
from ..environment import Base,jst, logger

class EnvSystemRole(ClireaBase):
    __tablename__ = 'EnvSystemRole'
    SystemRoleID = Column(Integer, primary_key=True, autoincrement=False)
    SystemRoleName = Column(String(255))

    def __init__(self, SystemRoleName, InsertDate=None, UpdateDate=None, SystemRoleID=None):
        self.SystemRoleID = SystemRoleID or None
        self.SystemRoleName = SystemRoleName
        self.InsertDate = InsertDate or datetime.now(jst)
        self.UpdateDate = UpdateDate or datetime.now(jst)

    def __str__(self):
        return f"""SystemRoleID: {self.SystemRoleID}
    SystemRoleName: {self.SystemRoleName}
    InsertDate: {self.InsertDate}
    UpdateDate: {self.UpdateDate}"""

    #create、1=system, 2=assistant, 3=user
    def CreateRole(session: sessionmaker) -> None:
        try:
            with session.begin():
                system = EnvSystemRole(SystemRoleName='system',SystemRoleID=1)
                assistant = EnvSystemRole(SystemRoleName='assistant',SystemRoleID=2)
                user = EnvSystemRole(SystemRoleName='user',SystemRoleID=3)
                session.add(system)
                session.add(assistant)
                session.add(user)
                session.commit()
        except Exception as e:
            logger.debug(f"エラー：{str(e)}")
            session.rollback()
