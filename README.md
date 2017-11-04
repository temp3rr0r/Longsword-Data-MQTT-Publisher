# LongswordStances

## Installation

Packages:
```
apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y
apt-get install python python-pip glib-2.0-dev libbluetooth-dev libreadline-dev libboost-python-dev pkg-config libboost-python-dev libboost-thread-dev libglib2.0-dev python-dev
```

Pip:
```
pip install AWSIoTPythonSDK
pip install gattlib
```

Source code samples
```
git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python/samples
python3 basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
```
