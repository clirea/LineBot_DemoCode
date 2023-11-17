import json
import numpy as np
from ..FrameworkModels import VectorModel
from ..environment import openai,client
from typing import List

def cosine_similarity(a, b):
    # 角括弧を削除し、コンマで分割
    a_values = a[1:-1].split(',')
    b_values = b[1:-1].split(',')
    # 文字列を浮動小数点数に変換
    a = np.array([float(value) for value in a_values])
    b = np.array([float(value) for value in b_values])
    # コサイン類似度を計算
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


#Vector化
def vectorize(text: str):
    res = client.embeddings.create(
        model='text-embedding-ada-002',
        input=text,
        encoding_format="float"
    )
    embedding = res['data'][0]['embedding']
    #str形式で返すため、json.dumpsを使用
    return json.dumps(embedding)


#ベクトルの類似度を計算して取得
def similarity(query:List[float], INDEX:List[VectorModel], top=10):
    results = map(
        lambda i: {
            'body': i['Data'],
            # ここでクエリと各文章のコサイン類似度を計算
            'similarity': cosine_similarity(i['Vector'], query)
            },
        INDEX
    )
    # コサイン類似度で降順（大きい順）にソート
    results = sorted(results, key=lambda i: i['similarity'], reverse=True)
    # 上位10件を返す。ない場合あるだけ返す。ない場合は空を返す
    if len(results) > top:
        return results[:top]
    else:
        return results

def similarity(query:str, INDEX:List[VectorModel], top=10):
    return similarity(vectorize(query), INDEX, top)
