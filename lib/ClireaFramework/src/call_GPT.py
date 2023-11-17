import asyncio
import nest_asyncio
from typing import List
from ..environment import GptModel,MaxTokens,encoding, logger, openai,client
from ..FrameworkModels import GptMessageModel
from concurrent.futures import ThreadPoolExecutor



#createmessage
def create_message(systemPrompt:str, messageList:List[GptMessageModel]=[], userMessage:str=None) -> List[GptMessageModel]:
    """
    :param systemPrompt: GPTのプロンプト
    :param messages: messageリスト
    :return: 
    """
    #messageListの形式を確認しGptMessageModelじゃない場合エラー
    for message in messageList:
        if not isinstance(message, GptMessageModel):
            raise ValueError("messageListの形式がGptMessageModelではありません")
        
    logger.debug(f"create_messageのsystemPrompt:{str(systemPrompt)}")
    systemMessage = GptMessageModel(role='system', content=systemPrompt)
    logger.debug(f"create_messageのsystemMessage:{str(systemMessage)}")
    messages = []
    messages.append(systemMessage)
    #""やNoneではない場合messageListに追加する
    if userMessage is not None and userMessage != "":
        messageList.append(GptMessageModel(role='user', content=userMessage))
    logger.debug(f"create_messageのmessageList:{str(messageList)}")
    #ChatGPTのトークン上限の為、全体のトークン数を確認しMaxTokensまでmessageListの内容を削る
    #messageListの内容を削る
    total_chars = len(encoding.encode(systemPrompt)) + sum([len(encoding.encode(msg.content)) for msg in messageList])
    logger.debug(f"create_messageのtotal_chars:{str(total_chars)}")
    while total_chars > MaxTokens and len(messageList) > 0:
        messageList.pop(0)
        total_chars = len(encoding.encode(systemPrompt)) + sum([len(encoding.encode(msg.content)) for msg in messageList])
    logger.debug(f"create_messageのtotal_chars:{str(total_chars)}")
    for message in messageList:
        messages.append(message)
    logger.debug(f"create_messageのmessages:{str(messages)}")
    return messages

#GPTへ送って返答を受け取る
def get_gpt_response(systemprompt: str,gptmodel: str = GptModel) -> str:
    try:        
        messages = create_message(systemprompt)
        #GPTへ投げる
        response_json = get_gpt_responses_json(messages,gptmodel)
        if response_json is not None:
            responseText = response_json.choices[0].message.content.strip() 
            logger.debug(f"GPTからの返答:{str(responseText)}")
            return responseText
        raise ValueError("ChatGPTからの返答がありません")
    except Exception as e:
        logger.error(f"{str(e)}")
        raise ValueError(f"{str(e)}") 
    
def get_gpt_response(systemPrompt:str, messageList:List[GptMessageModel]=[], userMessage:str=None, gptmodel:str=GptModel) -> str:
    try:
        messages = create_message(systemPrompt,messageList,userMessage)
        #GPTへ投げる
        response_json = get_gpt_responses_json(messages,gptmodel)
        if response_json is not None:
            responseText = response_json.choices[0].message.content.strip() 
            logger.debug(f"GPTからの返答:{str(responseText)}")
            return responseText
        raise ValueError("ChatGPTからの返答がありません")
    except Exception as e:
        logger.error(f"{str(e)}")
        raise ValueError(f"{str(e)}")
    
def GptMessageModels_to_json(messages: List[GptMessageModel]):
    return [message.to_json() for message in messages]

def get_gpt_responses_json(messages: List[GptMessageModel] ,gptmodel: str):
    try:
        
        logger.debug("GPT問い合わせ")
        response_json = client.chat.completions.create(
                                model=gptmodel,
                                messages=GptMessageModels_to_json(messages),
                            )
        logger.debug(f"GPT問い合わせ完了:{str(response_json)}")
        if response_json is not None:
            return response_json
        raise ValueError("ChatGPTからの返答がありませんでした。")
    except Exception as e:
        #TODO:エラー処理分岐処理追加：タイムアウト、トークン数超過等
        logger.error(f"エラー: {str(e)}")
        raise ValueError(f"エラーが発生しました。{str(e)}")
    
    
         
#非同期でGPTに投げる
def async_gpt_responses(prompts):
    try:
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        responses = []

        with ThreadPoolExecutor() as executor:
            tasks = [loop.run_in_executor(executor, get_gpt_response, prompt, GptModel) for prompt in prompts]
            responses = loop.run_until_complete(asyncio.gather(*tasks))

        return responses
    except Exception as e:
        #TODO:エラー処理分岐処理追加
        logger.error(f"{str(e)}")
        raise ValueError(f"{str(e)}")
