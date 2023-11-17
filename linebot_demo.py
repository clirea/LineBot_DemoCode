from concurrent.futures import ThreadPoolExecutor
from linebot.models import TextMessage, AudioSendMessage
from lib.ClireaFramework import *
import os
import asyncio
import nest_asyncio
cipher = AESCipher()
from lib_for_function import *
from prompt import Prompt
error_handler = SystemErrorMessage(lang="ja")  # 日本語のメッセージを得るためのインスタンスを作成

def linebot_demo(event,line_bot_api):    
    try:
        logger.info(f"処理開始")
        add_reply_text:str = "" # 返信するテキスト追加
        reply_text:str = ""       # 返信するテキスト
        _UserLineID:str = event.source.user_id

        if bucket_exists(BacketName):                    
            set_bucket_lifecycle(BacketName, FileAge)

        # テキストが来た場合
        if isinstance(event.message, TextMessage):                    
            user_message = event.message.text.strip()

            #user_messageが[cmd:CreateTable]の場合
            if user_message == "cmd:CreateTable":
                # テーブルを作成
                db.create_table()
                reply_text = "テーブルを作成しました。"
                return line_reply(line_bot_api, event,reply_text,_UserLineID,0)

            # 画像が来た場合
        elif event.message.type == "image":                    
            #TODO 画像の処理
            reply_text = "textか音声メッセージで入力をしてください。"
            return line_reply(line_bot_api, event,reply_text,_UserLineID,0)
        # スタンプが来た場合
        elif event.message.type == "sticker":
            keyword = event.message.keywords
            user_message = f"私の今の気持ちのキーワードです！！\n{keyword}\n\n私の今の気持ちを感じてそれに対して返答をしてください！"
        # 音声
        elif event.message.type == 'audio': 
            user_message = get_audio(ChannelAccessToken,OpenaiApiKey,event.message.id)
        else:
            reply_text = "textか音声メッセージで入力をしてください。"
            return line_reply(line_bot_api, event,reply_text,_UserLineID,0)

        
        user = db.get_user(None, _UserLineID)

        # ユーザーが登録されていない場合
        if user is None:
            # ユーザーが登録されていない場合                    
            displayname = get_profile(_UserLineID)

            #ユーザーを登録                    
            user = MstUsers(UserLineID=_UserLineID,VoiceOrText=EnumElement.VoiceOrTextIDs.Text,VoiceSpeed='normal',UserName=displayname)

            try:
                session = db.create_session()
                with session.begin():
                    session.add(user)
                    session.commit()
                session.close()
            except Exception as e:
                return handle_error(line_bot_api, event,  error_handler.get(error_code="msg_parse_error"),_UserLineID,e)
            
        # 使用するThreadPoolExecutor
        try:
            nest_asyncio.apply()
            loop = asyncio.get_event_loop()

            with ThreadPoolExecutor() as executor:
                moderation_future = loop.run_in_executor(executor, moderationsCheck, user_message)
                injection_future = loop.run_in_executor(executor, message_check, user_message)

                moderation_error_flag, moderation_error_list = loop.run_until_complete(moderation_future)
                injection = loop.run_until_complete(injection_future)

        except Exception as e:                            
            return handle_error(line_bot_api, event,  error_handler.get(error_code="msg_parse_error"),_UserLineID,e)

        #moderationチェック
        # moderation_error_flag, moderation_error_list = moderationsCheck(user_message)
        if moderation_error_flag:
            reply_text = "moderationチェックでエラーが発生しました。\n"
            reply_text += "エラー内容: " + ", ".join(moderation_error_list)  # エラーリストを文字列に変換して追加
            handle_error(line_bot_api, event, reply_text,_UserLineID,e)

        #プロンプトインジェクションチェックの追加
        if injection:
            reply_text = "プロンプトインジェクションと思われる入力があった為処理を中断します"
            return handle_error(line_bot_api, event,reply_text,_UserLineID,e)
            
        #GPTの返答を作成
        oldmessages = db.get_message_logs(user.UserID)    
        systemprompt = Prompt.MainPrompt
        reply_text = get_gpt_response_with_messages(systemprompt,create_message_models_from_message_log(oldmessages),user_message)
        
        if add_reply_text != "":
            reply_text = add_reply_text + reply_text
        #userのメッセージと返答を保存
        try:
            session = db.create_session()
            with session.begin():
                user = db.get_user(session, _UserLineID)
                MessageLogUser = TrnMessageLog(UserID=user.UserID,SystemRoleID=EnumElement.SystemRoleIDs.user, Message=cipher.encrypt(user_message))
                MessageLogAssistant = TrnMessageLog(UserID=user.UserID,SystemRoleID=EnumElement.SystemRoleIDs.assistant, Message=cipher.encrypt(reply_text))
                session.add(MessageLogUser)
                session.add(MessageLogAssistant)
                session.commit()                        
            session.close()
        except Exception as e:                    
            raise ValueError(f"{str(e)}")

        user = db.get_user(None, _UserLineID)
        num_reply = 3
        if user.VoiceOrText == EnumElement.VoiceOrTextIDs.Voice:
            blob_path = f'{user.UserLineID}/{event.message.id}.m4a'
            public_url, local_path, duration = text_to_speech(reply_text, BacketName, blob_path, "MANDARIN", "en-US", user.VoiceSpeed)
            return line_reply(line_bot_api,event,AudioSendMessage(original_content_url=public_url, duration=duration),_UserLineID)


        else:
            line_reply(line_bot_api, event,reply_text,_UserLineID,num_reply)

    except Exception as e:
        return handle_error(line_bot_api, event,  error_handler.get(error_code="msg_parse_error"),_UserLineID,e)