Instruction on how to connect your smart home devices to Robonomics through Home Assistant. There will be two methods to connect your device: directly to Raspberry Pi via zigbee2MQTT adapter or through Xiaomi Gateway.
# Requirements

* Raspberry Pi 4 or 3
* SD card and SD adapter
* Temperature sensor - [Keen Home RS-THP-MP-1.0](https://www.zigbee2mqtt.io/devices/RS-THP-MP-1.0.html) (or another [supported device](https://www.zigbee2mqtt.io/information/supported_devices.html))

### Method 1 (with zigbee2MQTT)
* Zigbee adapter [JetHome USB JetStick Z2](https://jhome.ru/catalog/parts/PCBA/293/) (or one of [supported](https://www.zigbee2mqtt.io/information/supported_adapters.html))

### Method 2 (with Xiaomi Gateway)
* Xiaomi Gateway (one of [supported](https://www.home-assistant.io/integrations/xiaomi_miio#xiaomi-gateway))
* [Mi Home app](https://play.google.com/store/apps/details?id=com.xiaomi.smarthome&hl=ru&gl=US) or HomeKit app

Also you can connect some devices directly through Mi Home app (for example, Vacuum Cleaner).

# Setup

1. Firstly you need to [setup Raspberry Pi](raspberry_setup.md) (also you can [use prepeared image](raspberry_image.md)).
2. Then you need to connect devices:
- [Connection with zigbee2MQTT](zigbee2MQTT.md)
- [Connection through Xiaomi Gateway](xiaomi_gateway.md)
- [Connect Vacuum Cleaner](vacuum_connect.md)
