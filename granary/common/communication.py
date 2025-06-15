#!/usr/bin/env python3

import json

import paho.mqtt.client as mqtt


class Zigbee2MQTTClient:
    def __init__(
        self,
        username: str,
        passwd: str,
        broker: str,
        port: int = 1883,
        logger=None,
    ) -> None:
        self._mqtt_username = username
        self._mqtt_passwd = passwd
        self._mqtt_broker = broker
        self._mqtt_port = port
        self._sub_topics = [("zigbee2mqtt/+", 0)]
        self._logger = logger

        self._bootstrap()

    def _bootstrap(self) -> None:
        # 建立 MQTT Client 物件
        self._client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2, "granary_zigbee2mqtt_client"
        )
        # 設定連接的帳號密碼
        self._client.username_pw_set(self._mqtt_username, self._mqtt_passwd)

        # 設定建立連線回呼函數
        self._client.on_connect = self._on_connect

        # 設定接收訊息回呼函數
        self._client.on_message = self._on_message

        # 設定斷線回呼函式
        self._client.on_disconnect = self._on_disconnect

        # 連線至 MQTT 伺服器（伺服器位址,連接埠）
        self._client.connect(
            self._mqtt_broker, self._mqtt_port, 60
        )  # 60 是 Keep alive 時間(秒)

    def _on_connect(self, client, userdata, flags, reason_code, properties):
        """
        建立連線（接收到 CONNACK）的 Callback 函數
        """
        if reason_code == 0:
            print("Connected to MQTT Broker!")
            # 每次連線之後，重新設定訂閱主題
            client.subscribe(self._sub_topics)
            print("Subscribed to Topic: {}".format(self._sub_topics))
            if self._logger:
                self._logger.info("Connected to MQTT Broker!")
                self._logger.info("Subscribed to Topic: {}".format(self._sub_topics))

        else:
            print("Connection failed, error code: {}".format(reason_code))
            if self._logger:
                self._logger.error(
                    "Connection failed, error code: {}".format(reason_code)
                )

    def _on_disconnect(self, client, userdata, flags, reason_code, properties):
        """
        斷線的 Callback 函數
        """
        if reason_code == 0:
            # success disconnect
            log_msg = "Disconnected from MQTT Broker"
            if self._logger:
                self._logger.info(log_msg)
        if reason_code > 0:
            # error processing
            log_msg = "Unexpected disconnection, error code: {}".format(reason_code)
            if self._logger:
                self._logger.error(log_msg)
        print(log_msg)

    def _on_message(self, client, userdata, msg):
        """
        接收訊息的 Callback 函數
        """
        try:
            # 將接收到的訊息轉換為 JSON 格式
            receive_msg = json.loads(msg.payload.decode("utf-8"))
            print("Received message: {}".format(receive_msg))
        except json.JSONDecodeError as e:
            # 如果 JSON 解析失敗，記錄錯誤訊息
            log_error = "Invalid JSON message received: {}, Error: {}".format(
                msg.payload.decode("utf-8"), e
            )
            print(log_error)
            if self._logger:
                self._logger.error(log_error)
            return

    def run(self):
        """
        程式執行
        """
        # 記錄程式開始
        print("Starting MQTT Communication...")
        if self._logger:
            self._logger.info("Starting  MQTT Communication...")

        # 進入無窮處理迴圈
        self._client.loop_forever()

    def __del__(self):
        if self._logger:
            self._logger.info("Disconnecting from MQTT Broker...")
        self._client.disconnect()
