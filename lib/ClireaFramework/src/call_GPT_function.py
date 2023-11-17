import json
from typing import List
from ..environment import GptFunctionModel, logger,client
import asyncio
from concurrent.futures import ThreadPoolExecutor
import nest_asyncio

#TODO:GPTFunctionModelのしように変更する

#GPTのfunctionの作成
"""
        functions=[
            {
                "name": "i_am_json",
                "description": "抽出された特徴を JSON として処理します。",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "title": {
                            "type": "string",
                            "description": "書籍のタイトルです",
                        },
                        "author": {
                            "type": "string",
                            "description": "書籍の著者です",
                        },
                        "reference": {
                            "type": "string",
                            "description": "情報の参照元 URL です",
                        },
                    },
                },
            }
        ],
"""
def create_function(name: str,
                     description: str,
                       properties: List[tuple],
                         parameters_type:str ='object'):
    """
    :param name: 関数名
    :param description: 関数の説明
    :param properties: プロパティのリスト
    :param parameters_type: パラメータのタイプ
    :return: 関数のJSON
    propertiesの内容は、{name, type, description}
    例：
        properties = [
            ("title", "string", "書籍のタイトルです"),
            ("author", "string", "書籍の著者です"),
            ("reference", "string", "情報の参照元 URL です"),
        ]
    """
    # create properties dictionary
    properties_dict = {}
    for prop in properties:
        prop_name, prop_type, prop_description = prop
        properties_dict[prop_name] = {"type": prop_type, "description": prop_description}

    # create function dictionary
    function_dict = {
        "name": name,
        "description": description,
        "parameters": {
            "type": parameters_type,
            "properties": properties_dict,
        }
    }

    return function_dict

#functionを配列にして返す関数
def add_function(function, add_function=None,functions=None):
    """
    :param function: 関数のJSON
    :param function2: 関数のJSON
    :param functions: 関数のリスト
    :return: 関数のリスト
    """
    if functions is None:
        functions = []
    functions.append(function)
    if add_function is not None:
        functions.append(add_function)
    return functions

#GPTのfunctionの実行及びリターン
def function_gpt(message, functions_,function_call_, gptmodel = GptFunctionModel):
    #functionsがNoneや空や配列ではない場合errorにする
    if functions_ is None or functions_ == [] or functions_ == "":
        logger.debug("functionsが空です")
        raise ValueError("functionsが空です")
    #messageがNoneや空や配列ではない場合errorにする
    if message is None or message == [] or message == "":
        logger.debug("messageが空です")
        raise ValueError("messageが空です")
    #function_callがNoneや空や配列ではない場合errorにする
    if function_call_ is None or function_call_ == [] or function_call_ == "":
        logger.debug("function_callが空です")
        raise ValueError("function_callが空です")    

    try:
        response = client.chat.completions.create(
            model=gptmodel,
            messages=message,
            temperature=0.6,
            functions=functions_,
            function_call=function_call_
        )

        response_message = response.choices[0].message    
    
        return json.loads(response_message.function_call.arguments)
    except json.JSONDecodeError:
        logger.error("JSON解析に失敗しました。")
        return {}  # JSONの解析に失敗した場合、空の辞書を返す


#非同期でGPTに投げる
def async_function_gpt_responses(prompts,gptmodel = GptFunctionModel):
    try:
        nest_asyncio.apply()
        loop = asyncio.get_event_loop()
        responses = []

        with ThreadPoolExecutor() as executor:
            tasks = [loop.run_in_executor(executor, function_gpt, prompt[0], prompt[1], prompt[2],gptmodel) for prompt in prompts]
            responses = loop.run_until_complete(asyncio.gather(*tasks))

        return responses
    except Exception as e:
        logger.error(f"エラー: {str(e)}")
        raise ValueError(f"エラーが発生しました。{str(e)}")