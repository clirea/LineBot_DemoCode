from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .ClireaBase import ClireaBase
from ..environment import Base,jst

class TrnVectorData(ClireaBase):
    __tablename__ = 'TrnVectorData'
    VectorDataID = Column(Integer, primary_key=True, autoincrement=False)
    UserID = Column(Integer, ForeignKey('MstUsers.UserID'))
    Data = Column(Text)
    Vector = Column(Text)
    MetaData = Column(Text)
    user = relationship("MstUsers", back_populates="vector_datas")

    def __init__(self, Data: str, UserID: int, Vector: str, MetaData: str, InsertDate: datetime = None, UpdateDate: datetime = None,VectorDataID:int=None):
        """
        :param Data: データ
        :param UserID: ユーザーのID
        :param Vector: ベクトル
        :param MetaData: メタデータ
        :param InsertDate?: データの作成日
        :param UpdateDate?: データの更新日        
        """
        self.VectorDataID = VectorDataID or None
        self.Data = Data
        self.UserID = UserID
        self.Vector = Vector
        self.MetaData = MetaData
        self.InsertDate = InsertDate or datetime.now(jst)
        self.UpdateDate = UpdateDate or datetime.now(jst)

    def __str__(self):
        return f"""VectorDataID: {self.VectorDataID}
    Data: {self.Data}
    UserID: {self.UserID}
    Vector: {self.Vector}
    MetaData: {self.MetaData}
    InsertDate: {self.InsertDate}
    UpdateDate: {self.UpdateDate}"""

