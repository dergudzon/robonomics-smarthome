# Connect Vacuum Cleaner to Robonomics

## Connect to Home Assistant

You need your vacuum to be connected to Mi Home app. If you haven't done this yet press `+` button on the top right corner, find your vacuum (it must be in connecting mode with long press to power button) and follow instructions in the app. For more details look at user manual of your vacuum.

Open Home Assistant web page with this address:
```
http://<raspberry_address>:8123
```

Go to `Integrations` tab, press `Add integration` and choose `Xiaomi Miio`:

![integration](media/integration.png)

Then fill your username (or phone) and password from Mi Home account and choose your country server:

![auth](media/auth.png)

Press `Submit` and choose your Vacuum (Robot vacuum in this example):

![vacuum](media/vacuum_int.png)

Then we need to setup action to control Vacuum through Robonomics. For that open a configuration file on your raspberry:

```bash
nano ~/.homeassistant/configuration.yaml
```

And add following to the end of the file:

```yaml
automation:
  - alias: "vacuum_start"
    trigger:
      platform: webhook
      webhook_id: "vacuum_start"
    action:
      service: vacuum.start
      target:
        entity_id:
          - vacuum.robot_vacuum

  - alias: "vacuum_pause"
    trigger:
      platform: webhook
      webhook_id: "vacuum_pause"
    action:
      service: vacuum.pause
      target:
        entity_id:
          - vacuum.robot_vacuum

  - alias: "vacuum_return_to_base"
    trigger:
      platform: webhook
      webhook_id: "vacuum_return_to_base"
    action:
      service: vacuum.return_to_base
      target:
        entity_id:
          - vacuum.robot_vacuum
```
Then download the script [control.py](scripts/control.py) to your python_scripts directory:
```bash
cd /srv/homeassistant/python_scripts
wget https://raw.githubusercontent.com/tubleronchik/robonomics-smarthome/main/scripts/control.py
```
Before running export your mnemonic seed:
```bash
export MNEMONIC_SEED=<mnemonic>
```
And run the script:
```bash
cd /srv/homeassistant/python_scripts
source /srv/homeassistant/bin/activate
python3 control.py
```
Now you can create datalog in your account to command robot to Start Cleaning, to Pause or to Return to Base. The message must be encrypted. you can send encrypted message with [send_datalog.py](scripts/send_datalog.py) script that you used in [Raspberry Setup](raspberry_setup.py) page.
Run the script in a new terminal with message to start cleaning:
```bash
cd /srv/homeassistant/python_scripts
source /srv/homeassistant/bin/activate
python3 send_datalog.py '{"agent": "vacuum_start"}'
```
to pause:
```bash
cd /srv/homeassistant/python_scripts
source /srv/homeassistant/bin/activate
python3 send_datalog.py '{"agent": "vacuum_pause"}'
```
to return to base:
```bash
cd /srv/homeassistant/python_scripts
source /srv/homeassistant/bin/activate
python3 send_datalog.py '{"agent": "vacuum_return_to_base"}'
```
