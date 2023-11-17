from sqlalchemy import Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .ClireaBase import ClireaBase
from ..environment import Base,jst


class TrnMessageLog(ClireaBase):
    __tablename__ = 'TrnMessageLog'
    MessageLogID = Column(Integer, primary_key=True, autoincrement=True)
    UserID = Column(Integer, ForeignKey('MstUsers.UserID'))
    SystemRoleID = Column(Integer)
    Message = Column(Text)
    user = relationship("MstUsers", back_populates="message_logs")

    def __init__(self, UserID: int, SystemRoleID: int, Message: str, InsertDate: datetime = None, UpdateDate: datetime = None, MessageLogID: int = None):
        """
        :param UserID: ユーザーのID
        :param SystemRoleID: ChatGPTとのメッセージのロール(1=system, 2=assistant, 3=user)
        :param Message: メッセージ
        :param InsertDate?: メッセージの作成日
        :param UpdateDate?: メッセージの更新日
        :param MessageLogID?: メッセージのID
        """
        
        self.MessageLogID = MessageLogID or None
        self.UserID = UserID
        self.SystemRoleID = SystemRoleID
        self.Message = Message
        #self.Message = encrypt_AES_ECB(Message)
        self.InsertDate = InsertDate or datetime.now(jst)
        self.UpdateDate = UpdateDate or datetime.now(jst)

    def __str__(self):
        return f"""MessageLogID: {self.MessageLogID}
    UserID: {self.UserID}
    SystemRoleID: {self.SystemRoleID}
    Message: {self.Message}
    InsertDate: {self.InsertDate}
    UpdateDate: {self.UpdateDate}"""
