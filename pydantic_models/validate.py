"""
VDA5050 Pydanticモデルの自動変換モジュール

このモジュールでは、メッセージタイプに基づいて、JSON文字列と様々なPydanticモデル間の
自動変換を行う機能を提供します。シンプルなメッセージタイプ＋データ構造を使用して、
JSONとPydanticモデル間の相互変換を実現します。
"""

import json
from typing import Dict, Any, Type, TypeVar, Optional
from pydantic import BaseModel

# VDA5050モデルのインポート
from pydantic_models.common import (
    Action, ActionParameter, BlockingType, ControlPoint, 
    Corridor, CorridorRefPoint, NodePosition, Trajectory
)
from pydantic_models.order import OrderMessage, Node, Edge
from pydantic_models.state import State
from pydantic_models.instantActions import InstantActions
from pydantic_models.connection import Connection

# 型変数の定義
T = TypeVar('T', bound=BaseModel)

# モデルタイプとクラスのマッピング
MODEL_TYPE_MAP: Dict[str, Type[BaseModel]] = {
    "Action": Action,
    "ActionParameter": ActionParameter,
    "BlockingType": BlockingType,
    "ControlPoint": ControlPoint,
    "Corridor": Corridor,
    "CorridorRefPoint": CorridorRefPoint,
    "NodePosition": NodePosition,
    "Trajectory": Trajectory,
    "OrderMessage": OrderMessage,
    "Node": Node,
    "Edge": Edge,
    "State": State,
    "InstantActions": InstantActions,
    "Connection": Connection,
}

def to_model(json_str: str) -> BaseModel:
    """
    JSON文字列からPydanticモデルに変換します。
    
    Args:
        json_str: message_typeとdataフィールドを含むJSON文字列
        
    Returns:
        変換されたPydanticモデル
        
    Raises:
        ValueError: JSONのパースに失敗した場合やサポートされていないmessage_typeの場合
    """
    try:
        # JSONをパース
        message = json.loads(json_str)
        
        # メッセージタイプとデータを取得
        message_type = message.get("message_type")
        data = message.get("data")
        
        if not message_type or not data:
            raise ValueError("JSONにmessage_typeまたはdataフィールドがありません")
        
        # モデルタイプに対応するクラスを取得
        model_class = MODEL_TYPE_MAP.get(message_type)
        if not model_class:
            raise ValueError(f"サポートされていないメッセージタイプです: {message_type}")
        
        # データからモデルインスタンスを作成
        return model_class.model_validate(data)
    
    except Exception as e:
        raise ValueError(f"JSONからモデルへの変換に失敗しました: {str(e)}")

def from_model(model: BaseModel) -> str:
    """
    Pydanticモデルをmessage_typeとdataフィールドを含むJSON文字列に変換します。
    
    Args:
        model: 変換するPydanticモデル
        
    Returns:
        message_typeとdataフィールドを含むJSON文字列
        
    Raises:
        ValueError: モデルのシリアル化に失敗した場合やサポートされていないモデルタイプの場合
    """
    try:
        # モデルのクラス名を取得
        model_type = model.__class__.__name__
        
        # サポートされているモデルタイプかチェック
        if model_type not in MODEL_TYPE_MAP:
            raise ValueError(f"サポートされていないモデルタイプです: {model_type}")
        
        # モデルをJSONに変換
        model_data = json.loads(model.model_dump_json())
        
        # メッセージ構造を作成
        message = {
            "message_type": model_type,
            "data": model_data
        }
        
        # JSON文字列に変換
        return json.dumps(message)
    
    except Exception as e:
        raise ValueError(f"モデルからJSONへの変換に失敗しました: {str(e)}")

def create_message(message_type: str, data: Dict[str, Any]) -> str:
    """
    指定されたメッセージタイプとデータからJSON文字列を作成します。
    
    Args:
        message_type: メッセージタイプ("Action", "OrderMessage"など)
        data: モデルデータ
        
    Returns:
        message_typeとdataフィールドを含むJSON文字列
        
    Raises:
        ValueError: サポートされていないメッセージタイプの場合
    """
    if message_type not in MODEL_TYPE_MAP:
        raise ValueError(f"サポートされていないメッセージタイプです: {message_type}")
    
    message = {
        "message_type": message_type,
        "data": data
    }
    
    return json.dumps(message)

def get_model_class(message_type: str) -> Optional[Type[BaseModel]]:
    """
    メッセージタイプに対応するPydanticモデルクラスを取得します。
    
    Args:
        message_type: メッセージタイプ("Action", "OrderMessage"など)
        
    Returns:
        対応するPydanticモデルクラス、またはNone(サポートされていない場合)
    """
    return MODEL_TYPE_MAP.get(message_type) 