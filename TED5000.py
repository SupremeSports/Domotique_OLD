from xml.etree import ElementTree
from datetime import datetime
import requests

class TED5000:
    def __init__(self, url="http://supremesports.ddns.net:8081/api/LiveData.xml"):    
        self.url = url
        self.reload()

    def reload(self):
        response = requests.get(self.url)
        self.root = ElementTree.fromstring(response.content)

    def get(self, *tags):
        xpath = "./"+"/".join(tags)
        node = self.root.find(xpath)
        return float(node.text)

if __name__=="__main__":
    #Tests
    ted = TED5000()
    hour = ted.get("GatewayTime","Hour")
    print(hour)
    voltage_now = ted.get("Voltage","MTU1","VoltageNow")
    print(voltage_now)
