import json

class GptFunctionPropertiesModel:
    def __init__(self, title: str, type: str, description: str):
        self.title = title
        self.type = type
        self.description = description
    
    def __str__(self):
        # JSON
        return json.dumps({
            self.title: {
                "type": self.type,
                "description": self.description
            }
        })
    
    def __repr__(self):
        return f'GptFunctionPropertiesModel(title="{self.title}", type="{self.type}", description="{self.description}")'

class GptFunctionParametersModel:
    def __init__(self, type: str, properties: dict):
        self.type = type
        self.properties = properties
    
    def __str__(self):
        # JSON
        return json.dumps({
            "type": self.type,
            "properties": self.properties
        })
    
    def __repr__(self):
        return f'GptFunctionParametersModel(type="{self.type}", properties={self.properties})'
    
class GptFunctionModel:
    def __init__(self, name: str, description: str, parameters: GptFunctionParametersModel):
        self.name = name
        self.description = description
        self.parameters = parameters
    
    def __str__(self): 
        # JSON
        return json.dumps({
            "name": self.name,
            "description": self.description,
            "parameters": json.loads(str(self.parameters))
        })
    
    def __repr__(self):
        return f'GptFunctionModel(name="{self.name}", description="{self.description}", parameters={self.parameters})'

# JSON変換のために、propertiesを作成する関数
def create_properties(properties_data):
    properties = {}
    for key, value in properties_data.items():
        prop_model = GptFunctionPropertiesModel(title=key, type=value['type'], description=value['description'])
        properties[key] = json.loads(str(prop_model))
    return properties

# # 使用例
# properties = create_properties({
#     "title": {
#         "type": "string",
#         "description": "書籍のタイトルです",
#     },
#     "author": {
#         "type": "string",
#         "description": "書籍の著者です",
#     },
#     "reference": {
#         "type": "string",
#         "description": "情報の参照元 URL です",
#     },
# })
# parameters = GptFunctionParametersModel(type="object", properties=properties)
# function = GptFunctionModel(name="i_am_json", description="抽出された特徴を JSON として処理します。", parameters=parameters)

# print(function)