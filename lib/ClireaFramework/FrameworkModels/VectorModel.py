#参考データ
"""
    {
        "Data"(str): "パイナップルは、(以下略)"
        "Vector"(配列？): [0.12345, 0.12345, 0.12345, 以下略(1500次元)]
        "MetaData"(str): "text-embedding-ada-002"
    }
"""
from .. FrameworkEntities import TrnVectorData
from typing import List
class VectorModel:
    def __init__(self, Data: str, Vector: List[float], MetaData: str):
        self.Data = Data
        self.Vector = Vector
        self.MetaData = MetaData
    
    def __str__(self):
        return f'Data: {self.Data}\nVector: {self.Vector}\nMetaData: {self.MetaData}'
    
    def __repr__(self):
        return f'VectorModel(Data="{self.Data}", Vector={self.Vector}, MetaData="{self.MetaData}")'
    
def convert_TrnVectorData_to_VectorModel(data:TrnVectorData)->VectorModel:
    return VectorModel(data.Data,data.Vector,data.MetaData)
 
def convert_TrnVectorData_to_VectorModel(data:List[TrnVectorData])->List[VectorModel]:
    return List(map(convert_TrnVectorData_to_VectorModel,data))
 