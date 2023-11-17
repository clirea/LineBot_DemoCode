from sqlalchemy import inspect,desc
from sqlalchemy.orm import sessionmaker
import sqlalchemy
import os
from typing import List, Dict
from ..environment import Base, _DEBUG, logger,username,password,server,database,unix_socket_path
from .AESCipher import AESCipher
from ..FrameworkEntities.EnvSystemRole import EnvSystemRole
from ..FrameworkEntities.TrnMessageLog import TrnMessageLog
from ..FrameworkEntities.MstUsers import MstUsers
cipher = AESCipher()

class db():

    #DBtableの作成
    def create_table():
        """これはDBのテーブルを作成する関数です。"""
        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=username,
                password=password,
                database=database,
                query={"unix_socket": unix_socket_path},
            ),
        )

        Base.metadata.create_all(bind=engine)
        logger.debug("DBtableの作成")

    def create_data(session):
        #roleの作成
        EnvSystemRole.CreateRole(session)
        logger.debug("roleの作成")
        

    #DBsessionの作成
    def create_session() -> sessionmaker:
        """これはDBのセッションを作成する関数です。"""

        logger.debug("DBsessionの作成")            

        engine = sqlalchemy.create_engine(
            sqlalchemy.engine.url.URL.create(
                drivername="mysql+pymysql",
                username=username,
                password=password,
                database=database,
                query={"unix_socket": unix_socket_path},
            ),
        )

        logger.debug("engineの作成")
        Session = sessionmaker(bind=engine)
        logger.debug("Sessionの作成")
        session = Session()
        logger.debug("sessionの作成")
        return session
    
    def get_system_role() -> List[EnvSystemRole]:
        """これはroleをすべて取得する関数です。"""
        session = db.create_session()
        roles = session.query(EnvSystemRole).all()
        session.close()
        return roles

    
    def get_user(session, UserLineID: int) -> MstUsers:
        """
        これはUserLineIDでユーザーを取得する関数です。
        """
        if UserLineID == 0:
            return None

        user = None
        if session is None:
            with db.create_session() as session:
                user = session.query(MstUsers).filter(MstUsers.UserLineID == UserLineID).one_or_none()
        else:
            user = session.query(MstUsers).filter(MstUsers.UserLineID == UserLineID).one_or_none()

        return user
    
    def get_message_logs(UserID:int, limit:int = 6) -> List[TrnMessageLog]:
        """
        これはUserLineIDでメッセージログを取得する関数です。
        並び順は新しい順で取得し、逆順にします。
        """  
        session = db.create_session()
        message_logs:List[TrnMessageLog] = session.query(TrnMessageLog).filter(TrnMessageLog.UserID == UserID).order_by(TrnMessageLog.MessageLogID.desc()).limit(limit).all()
        message_logs.reverse()
        
        #復号化を行う(decrypt_AES_ECB)
        for message_log in message_logs:
            message_log.Message = cipher.decrypt(message_log.Message)
        session.close()
        return message_logs
    