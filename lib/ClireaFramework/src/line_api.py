import json
import requests
from flask import jsonify
from flask import jsonify
from linebot import LineBotApi
from linebot.models import MessageEvent, TextSendMessage,AudioSendMessage, QuickReply, QuickReplyButton, MessageAction
from ..environment import _DEBUG, logger, ChannelAccessToken,ReplyCount, GptModel
from ..src.call_GPT import get_gpt_response



# # テキストとクイックリプライのラベルとテキストを設定する関数
def create_quick_reply_message(text: str, quick_reply_dict: dict):
    """
    :param text: テキスト
    :param quick_reply_dict: クイックリプライのラベルとテキストの辞書
    :return: Lineのメッセージオブジェクト
    """
    quick_reply_items = []
    for label, reply_text in quick_reply_dict.items():
        logger.debug(f"クイックリプライ作成：{str(reply_text)}")
        action = MessageAction(label=label, text=reply_text)
        button = QuickReplyButton(action=action)
        quick_reply_items.append(button)
    quick_reply = QuickReply(items=quick_reply_items)
    logger.debug(f"{str(text)}のクイックリプライ作成")
    message = TextSendMessage(text=text, quick_reply=quick_reply)
    logger.debug(str(message))
    return message


# # クイックリプライを追加する関数
def add_quick_reply_items(message, *args):

    """
    :param message: Lineのメッセージオブジェクト
    :param args: クイックリプライのラベルとテキスト
    :return: Lineのメッセージオブジェクト
    """
    for i in range(0, len(args), 2):
        label = args[i]
        reply_text = args[i+1]
        action = MessageAction(label=label, text=reply_text)
        button = QuickReplyButton(action=action)
        message.quick_reply.items.append(button)
    return message

# クイックリプライを追加する関数
def add_quick_reply_items_template(message, quick_reply_list):

    """
    :param message: Lineのメッセージオブジェクト
    :param quick_reply_list: クイックリプライのラベルとテキストのリスト
    quick_reply_listの内容は
    [ラベル1, テキスト1, ラベル2, テキスト2, ...]
    :return: Lineのメッセージオブジェクト
    """
    for i in range(0, len(quick_reply_list), 2):
        label = quick_reply_list[i]
        reply_text = quick_reply_list[i + 1]
        action = MessageAction(label=label, text=reply_text)
        button = QuickReplyButton(action=action)
        message.quick_reply.items.append(button)
    return message



def get_profile(userLineId: str) -> requests.Response:
    """
    :param userId: ユーザーID
    :return: ユーザーのプロフィール
    profileの内容は    
        profile.display_name #-> 表示名
        profile.user_id #-> ユーザーID
        profile.image_url #-> 画像のURL
        profile.status_message #-> ステータスメッセージ    
    """
    #DEBUG
    if _DEBUG == True:
        return "テストユーザー"
    url = 'https://api.line.me/v2/bot/profile/' + userLineId
    headers = {
        "Content-Type": "application/json; charset=UTF-8",
        "Authorization": "Bearer " + ChannelAccessToken,
    }
    response = requests.get(url, headers=headers, timeout=5)  # Timeout after 5 seconds
    return response.json()['displayName']


def line_reply(line_bot_api: LineBotApi, event: MessageEvent, reply_text,UserLineID,num_replies=ReplyCount):
    if _DEBUG == False:
        # reply_textが文字列の場合
        if isinstance(reply_text, str):
            if num_replies == 0:
                message = TextSendMessage(text=reply_text)
            else:
                message = generate_quick_reply(reply_text,UserLineID,num_replies)
        # reply_textがTextSendMessageのインスタンスの場合
        elif isinstance(reply_text, TextSendMessage):
            message = reply_text
        elif isinstance(reply_text, AudioSendMessage):
            message = reply_text
        else:
            raise TypeError("Unsupported type for reply_text")

        line_bot_api.reply_message(event.reply_token, message)
        return jsonify({'message': 'ok'})
    if _DEBUG == True:
        # reply_textが文字列の場合
        if isinstance(reply_text, str):
            if num_replies == 0:
                message = TextSendMessage(text=reply_text)
            else:
                message = generate_quick_reply(reply_text,UserLineID,num_replies)
        # reply_textがTextSendMessageのインスタンスの場合
        elif isinstance(reply_text, TextSendMessage):
            message = reply_text
        elif isinstance(reply_text, AudioSendMessage):
            message = reply_text
        else:
            raise TypeError("Unsupported type for reply_text")
        
        if isinstance(message, AudioSendMessage):
            pass
        else:
            print(message.text)
            return message.text

# #Exceptionを関数化
def handle_error(line_bot_api, event, ErrorMessage: str,userLineID, e: Exception = None) -> dict:
    
    """
    LineBotApiのreply_messageを使ってエラーメッセージを返す関数
    :param line_bot_api: LineBotApiのインスタンス
    :param event: Lineのイベントオブジェクト
    :param ErrorMessage: エラーメッセージ
    """
    logger.error(f"errormessage: {ErrorMessage}")
    logger.error(f"エラー: {str(e)}")
    reply_text = ErrorMessage
    #DEBUG
    if _DEBUG == True:
        print(reply_text)
        return reply_text
    #RELEASE
    return line_reply(line_bot_api, event,reply_text,userLineID,0)


#gptMessageへの返答例を3つ作成
def generate_quick_reply(gptMessage: str,UserLineID: str, num_replies: int=3) -> dict:
    # 1. GPTに5つの返答例をJSON形式で取得するプロンプトを作成
    instruction = f"\n"
    json_structure = "\n".join([f"reply{i}: '回答{i}'\n" for i in range(1, num_replies+1)])
    #last_message = db.get_latest_message_log(UserLineID, 1)
    prompt = f"""
========Instruction========
For the following INPUT, conceive a succinct one-sentence responses that would provide the relevant information to answer the INPUT, generate {num_replies} random versions, and return them in the specified JSON format.
#Guideline: Responses will be used as reply examples in Line's quick replies, so ensure they are concise and within 20 characters.
#Guideline: Only return the JSON format.
#Guideline: Ensure your responses are specific examples based on the context of the INPUT.
#Condition: Match the output to the input language.

Format:
{{
{json_structure}
}}

Below is the context.

========INPUT========
{gptMessage}

""" 
    
    # GPTに応答を求める
    logger.debug(f"prompt:{str(prompt)}")
    responseText = get_gpt_response(prompt,GptModel)
    logger.debug(f"response:{str(responseText)}")

    try:
        response_data = json.loads(responseText)
    except json.JSONDecodeError:
        logger.error("GPTの応答が正しくありません。")
        return TextSendMessage(text=gptMessage) 
    
    # 2. クイックリプライのラベルとテキストを設定
    quick_reply_dict = {}
    for i in range(1, num_replies+1):
        label = response_data.get(f"reply{i}", f"{i}")
        reply_text = response_data.get(f"reply{i}", f"{i}")
        
        # 20文字以上の場合は切り詰める
        if len(label) > 20:
            label = label[:20]
        if len(reply_text) > 20:
            reply_text = reply_text[:20]
        
        quick_reply_dict[label] = reply_text
    # クイックリプライを作成
    logger.debug("クイックリプライ作成")
    return create_quick_reply_message(gptMessage, quick_reply_dict)
