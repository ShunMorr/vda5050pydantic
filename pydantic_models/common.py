"""
VDA5050プロトコルにおける共通データモデル定義モジュール。

このモジュールは、複数のVDA5050メッセージタイプで共通して使用されるデータモデルを
Pydanticモデルとして定義しています。これにより、コードの重複を減らし、
モデル定義の一貫性を確保します。

参照: VDA5050 v2.1.0
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class BlockingType(Enum):
    """
    アクションのブロッキングタイプを定義する列挙型。
    
    NONE: 他のアクションや移動と並行して実行可能
    SOFT: 移動は不可だが他のアクションと並行して実行可能
    HARD: 他のアクションや移動と並行して実行不可(このアクションのみ実行可能)
    """
    NONE = 'NONE'
    SOFT = 'SOFT'
    HARD = 'HARD'


class ActionParameter(BaseModel):
    """
    アクションパラメータを表すモデル。
    
    キーと値のペアとして定義され、アクションの実行に必要な追加情報を提供します。
    様々なデータ型(配列、真偽値、数値、文字列、オブジェクト)の値をサポートします。
    """
    key: str = Field(
        ...,
        description='The key of the action parameter.',
        examples=['duration', 'direction', 'signal'],
    )
    value: Union[List[Any], bool, float, str, Dict[str, Any]] = Field(
        ...,
        description='The value of the action parameter',
        examples=[103.2, 'left', True, ['arrays', 'are', 'also', 'valid']],
    )


class Action(BaseModel):
    """
    AGVが実行すべきアクションを表すモデル。
    
    アクションタイプ、一意のID、実行条件(ブロッキングタイプ)および
    オプションのパラメータからなります。各アクションはAGVの状態(actionState)
    と対応付けられます。
    """
    actionType: str = Field(
        ...,
        description='Name of action as described in the first column of "Actions and Parameters". Identifies the function of the action.',
    )
    actionId: str = Field(
        ...,
        description='Unique ID to identify the action and map them to the actionState in the state. Suggestion: Use UUIDs.',
    )
    actionDescription: Optional[str] = Field(
        None, description='Additional information on the action.'
    )
    blockingType: BlockingType = Field(
        ...,
        description='Regulates if the action is allowed to be executed during movement and/or parallel to other actions.\nnone: action can happen in parallel with others, including movement.\nsoft: action can happen simultaneously with others, but not while moving.\nhard: no other actions can be performed while this action is running.',
    )
    actionParameters: Optional[List[ActionParameter]] = Field(
        None,
        description='Array of actionParameter-objects for the indicated action e. g. deviceId, loadId, external Triggers.',
    )


class NodePosition(BaseModel):
    """
    マップ上のノード位置を定義するモデル。
    
    ノードの座標(x, y)、向き(theta)、許容偏差などを含みます。
    各階には独自のマップがあり、すべてのマップは同じプロジェクト固有のグローバル座標系を使用します。
    """
    x: float = Field(
        ...,
        description='X-position on the map in reference to the map coordinate system. Precision is up to the specific implementation.',
    )
    y: float = Field(
        ...,
        description='Y-position on the map in reference to the map coordinate system. Precision is up to the specific implementation.',
    )
    theta: Optional[float] = Field(
        None,
        ge=-3.14159265359,
        le=3.14159265359,
        description='Absolute orientation of the AGV on the node. \nOptional: vehicle can plan the path by itself.\nIf defined, the AGV has to assume the theta angle on this node. If previous edge disallows rotation, the AGV must rotate on the node. If following edge has a differing orientation defined but disallows rotation, the AGV is to rotate on the node to the edges desired rotation before entering the edge.',
    )
    allowedDeviationXY: Optional[float] = Field(
        None,
        ge=0.0,
        description='Indicates how exact an AGV has to drive over a node in order for it to count as traversed.\nIf = 0: no deviation is allowed (no deviation means within the normal tolerance of the AGV manufacturer).\nIf > 0: allowed deviation-radius in meters. If the AGV passes a node within the deviation-radius, the node is considered to have been traversed.',
    )
    allowedDeviationTheta: Optional[float] = Field(
        None,
        ge=0.0,
        le=3.141592654,
        description='Indicates how big the deviation of theta angle can be. \nThe lowest acceptable angle is theta - allowedDeviationTheta and the highest acceptable angle is theta + allowedDeviationTheta.',
    )
    mapId: str = Field(
        ...,
        description='Unique identification of the map in which the position is referenced.\nEach map has the same origin of coordinates. When an AGV uses an elevator, e.g., leading from a departure floor to a target floor, it will disappear off the map of the departure floor and spawn in the related lift node on the map of the target floor.',
    )
    mapDescription: Optional[str] = Field(
        None, description='Additional information on the map.'
    )


class ControlPoint(BaseModel):
    """
    NURBSを定義する制御点のモデル。
    
    座標(x, y)と重み(weight)で構成されます。
    重みは、この制御点がカーブに与える引力の強さを定義します。
    """
    x: float = Field(
        ..., description='X coordinate described in the world coordinate system.'
    )
    y: float = Field(
        ..., description='Y coordinate described in the world coordinate system.'
    )
    weight: Optional[float] = Field(
        None,
        ge=0.0,
        description='The weight, with which this control point pulls on the curve. When not defined, the default will be 1.0.',
    )


class Trajectory(BaseModel):
    """
    AGVが経路上を移動する際の軌跡を定義するNURBS(非一様有理Bスプライン)モデル。
    
    次数(degree)、ノットベクトル、制御点のリストから構成され、
    エッジに沿ってAGVが移動すべき経路を詳細に定義します。
    """
    degree: int = Field(
        ...,
        ge=1,
        description='Defines the number of control points that influence any given point on the curve. Increasing the degree increases continuity. If not defined, the default value is 1.',
    )
    knotVector: List[float] = Field(
        ...,
        description='Sequence of parameter values that determines where and how the control points affect the NURBS curve. knotVector has size of number of control points + degree + 1.',
    )
    controlPoints: List[ControlPoint] = Field(
        ...,
        description='List of JSON controlPoint objects defining the control points of the NURBS, which includes the beginning and end point.',
    )


class CorridorRefPoint(Enum):
    """
    回廊(corridor)の基準点を定義する列挙型。
    
    KINEMATICCENTER: 車両の運動学的中心を基準とする
    CONTOUR: 車両の輪郭(外形)を基準とする
    """
    KINEMATICCENTER = 'KINEMATICCENTER'
    CONTOUR = 'CONTOUR'


class Corridor(BaseModel):
    """
    車両が軌道から逸脱可能な境界を定義する回廊モデル。
    
    障害物回避などのために、車両が軌道から左右にどれだけ逸脱できるかを定義します。
    回廊の基準点(車両の中心または輪郭)も指定可能です。
    """
    leftWidth: float = Field(
        ...,
        ge=0.0,
        description='Defines the width of the corridor in meters to the left related to the trajectory of the vehicle.',
    )
    rightWidth: float = Field(
        ...,
        ge=0.0,
        description='Defines the width of the corridor in meters to the right related to the trajectory of the vehicle.',
    )
    corridorRefPoint: Optional[CorridorRefPoint] = Field(
        None,
        description='Defines whether the boundaries are valid for the kinematic center or the contour of the vehicle.',
    ) 