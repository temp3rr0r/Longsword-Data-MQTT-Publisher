# LongswordStances

## Installation

apt-get update -y && apt-get upgrade -y && apt-get dist-upgrade -y
apt-get install python3
apt-get install python3-pip
apt-get install glib-2.0
pip3 install AWSIoTPythonSDK
pip3 install gattlib

git clone https://github.com/aws/aws-iot-device-sdk-python.git
cd aws-iot-device-sdk-python/samples
python3 basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>
