"""
VDA5050 Pydanticモデルのインポートテスト

このファイルは、各モジュールが正しくインポートできることを確認するためのものです。
"""

# 各モジュールからのインポートテスト
from pydantic_models.common import (
    Action,
    ActionParameter,
    BlockingType,
    ControlPoint,
    Corridor,
    CorridorRefPoint,
    NodePosition,
    Trajectory,
)

from pydantic_models.instantActions import InstantActions

from pydantic_models.order import (
    Edge,
    Node,
    OrderMessage,
)

from pydantic_models.state import (
    ActionState,
    ActionStatus,
    AgvPosition,
    BatteryState,
    EdgeState,
    Error,
    ErrorLevel,
    ErrorReference,
    EStop,
    Information,
    InfoLevel,
    InfoReference,
    Load,
    Map,
    MapStatus,
    NodeState,
    OperatingMode,
    SafetyState,
    SimplifiedNodePosition,
    State,
    Velocity,
)

from pydantic_models.visualization import Visualization

from pydantic_models.connection import Connection, ConnectionState

from pydantic_models.factsheet import (
    AgvAction,
    AgvClass,
    AgvFactsheet,
    AgvGeometry,
    AgvKinematic,
    LoadSpecification,
    LocalizationType,
    NavigationType,
    PhysicalParameters,
    ProtocolFeatures,
    ProtocolLimits,
    Support,
    TypeSpecification,
    VehicleConfig,
)

print("All imports successful!") 