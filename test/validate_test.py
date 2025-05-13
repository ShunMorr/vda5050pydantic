"""
VDA5050 メッセージ変換のテスト

このスクリプトは、pydantic_models.validateモジュールの機能をテストします。
"""

from datetime import datetime
import json
from pydantic_models.validate import to_model, from_model, create_message
from pydantic_models.common import Action, ActionParameter, BlockingType

def test_action_serialization():
    """Actionモデルのシリアル化と逆シリアル化をテスト"""
    # テスト用のActionオブジェクトを作成
    action = Action(
        actionType="startCharging",
        actionId="action_001",
        blockingType=BlockingType.HARD,
        actionParameters=[
            ActionParameter(key="duration", value=300),
            ActionParameter(key="connector", value="type2")
        ]
    )
    
    # モデルをJSON文字列に変換
    json_str = from_model(action)
    print(f"シリアル化されたAction: {json_str}")
    
    # JSON文字列を解析して内容を確認
    message = json.loads(json_str)
    assert message["message_type"] == "Action"
    assert message["data"]["actionType"] == "startCharging"
    assert message["data"]["actionId"] == "action_001"
    assert message["data"]["blockingType"] == "HARD"
    
    # JSON文字列をモデルに戻す
    restored_action = to_model(json_str)
    print(f"復元されたAction: {restored_action}")
    
    # 復元されたモデルが元のモデルと同じ内容を持つことを確認
    assert isinstance(restored_action, Action)
    assert restored_action.actionType == action.actionType
    assert restored_action.actionId == action.actionId
    assert restored_action.blockingType == action.blockingType
    assert len(restored_action.actionParameters) == len(action.actionParameters)
    
    print("Actionのシリアル化テスト成功!\n")

def test_create_message():
    """create_message関数をテスト"""
    # Actionのデータを定義
    action_data = {
        "actionType": "pauseOrder",
        "actionId": "pause_123",
        "blockingType": "NONE"
    }
    
    # メッセージを作成
    json_str = create_message("Action", action_data)
    print(f"create_messageで作成されたメッセージ: {json_str}")
    
    # メッセージを解析して内容を確認
    message = json.loads(json_str)
    assert message["message_type"] == "Action"
    assert message["data"]["actionType"] == "pauseOrder"
    
    # メッセージからモデルを復元
    model = to_model(json_str)
    assert isinstance(model, Action)
    assert model.actionType == "pauseOrder"
    
    print("create_message関数のテスト成功!\n")

def test_ros2_usecase():
    """ROS2での使用例をシミュレート"""
    print("ROS2ユースケースのシミュレーション:")
    
    # パブリッシャー側でActionモデルを作成
    action = Action(
        actionType="cancelOrder",
        actionId="cancel_xyz",
        blockingType=BlockingType.NONE
    )
    
    # モデルをJSON文字列に変換（ROS2のString型メッセージとして送信する想定）
    ros2_message_data = from_model(action)
    print(f"ROS2で送信するメッセージ: {ros2_message_data}")
    
    # サブスクライバー側でメッセージを受信し、モデルに復元
    received_model = to_model(ros2_message_data)
    print(f"受信側で復元されたモデル: {received_model}")
    
    # モデルのタイプに基づいた処理
    if isinstance(received_model, Action):
        print(f"Actionを受信: actionType={received_model.actionType}, actionId={received_model.actionId}")
    
    print("ROS2ユースケースのシミュレーション成功!\n")

if __name__ == "__main__":
    print("=== VDA5050メッセージ変換テスト開始 ===\n")
    
    test_action_serialization()
    test_create_message()
    test_ros2_usecase()
    
    print("=== すべてのテストが成功しました ===") 