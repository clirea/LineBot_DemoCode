from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .ClireaBase import ClireaBase
from ..environment import Base,jst

class MstUsers(ClireaBase):
    __tablename__ = 'MstUsers'
    UserID = Column(Integer, primary_key=True, autoincrement=True)
    UserLineID = Column(String(255))
    VoiceOrText = Column(Integer)
    VoiceSpeed = Column(String(20))
    UserName = Column(String(255))
    message_logs = relationship("TrnMessageLog", back_populates="user")
    vector_datas = relationship("TrnVectorData", back_populates="user")

    def __init__(self, UserLineID: str, VoiceOrText: int, VoiceSpeed: str, UserName: str, InsertDate: datetime = None, UpdateDate: datetime = None, UserID: int = None):
        """
        :param UserID?: ユーザーのID
        :param UserLineID: ユーザーのLineID
        :param VoiceOrText: ユーザーがテキストか音声か(1=テキスト, 2=音声)
        :param VoiceSpeed: ユーザーの音声の速さ(slow, normal, fast)
        :param UserName: ユーザーの名前
        :param InsertDate?: ユーザーの作成日
        :param UpdateDate?: ユーザーの更新日
        """
        self.UserID = UserID or None
        self.UserLineID = UserLineID
        self.VoiceOrText = VoiceOrText
        self.VoiceSpeed = VoiceSpeed
        self.UserName = UserName
        self.InsertDate = InsertDate or datetime.now(jst)
        self.UpdateDate = UpdateDate or datetime.now(jst)

    def __str__(self):
        return f"""UserID: {self.UserID}
    UserLineID: {self.UserLineID}
    VoiceOrText: {self.VoiceOrText}
    VoiceSpeed: {self.VoiceSpeed}
    UserName: {self.UserName}
    InsertDate: {self.InsertDate}
    UpdateDate: {self.UpdateDate}"""
