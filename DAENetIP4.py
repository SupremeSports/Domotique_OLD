from xml.etree import ElementTree
from datetime import datetime
import requests

class DAENetIP4:
    def __init__(self, url="http://supremesports.ddns.net:8082/current_state.xml?pw=abcd1234"):    
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
    dae = DAENetIP4()
    pis = dae.get("AnalogInput4","Value")
    print(pis)
	