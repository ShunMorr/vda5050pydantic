"""
VDA5050 Pydanticモデルのバリデーションテスト

このファイルは、モデルが正しくバリデーションされることを確認するためのものです。
"""

from datetime import datetime
from pydantic_models.common import Action, ActionParameter, BlockingType
from pydantic_models.instantActions import InstantActions


def test_action_parameter():
    # ActionParameterのテスト
    param = ActionParameter(key="duration", value=10.5)
    print(f"ActionParameter created: {param.model_dump_json()}")
    
    # 文字列値のテスト
    param_str = ActionParameter(key="direction", value="left")
    print(f"ActionParameter with string: {param_str.model_dump_json()}")
    
    # リスト値のテスト
    param_list = ActionParameter(key="options", value=["option1", "option2"])
    print(f"ActionParameter with list: {param_list.model_dump_json()}")


def test_action():
    # Actionのテスト
    action = Action(
        actionType="startCharging",
        actionId="action_001",
        blockingType=BlockingType.HARD,
        actionParameters=[
            ActionParameter(key="duration", value=300),
            ActionParameter(key="connector", value="type2")
        ]
    )
    print(f"Action created: {action.model_dump_json()}")


def test_instant_actions():
    # InstantActionsのテスト
    instant_actions = InstantActions(
        headerId=1,
        timestamp=datetime.now(),
        version="1.0.0",
        manufacturer="TestManufacturer",
        serialNumber="AGV123",
        actions=[
            Action(
                actionType="cancelOrder",
                actionId="cancel_001",
                blockingType=BlockingType.NONE
            ),
            Action(
                actionType="pause",
                actionId="pause_001",
                blockingType=BlockingType.HARD
            )
        ]
    )
    print(f"InstantActions created: {instant_actions.model_dump_json()}")


if __name__ == "__main__":
    print("Running validation tests...")
    test_action_parameter()
    test_action()
    test_instant_actions()
    print("All tests completed successfully!") 