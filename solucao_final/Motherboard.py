import json
import sys
import azure.iot.hub as iotHub
import azure.iot.device as iotDevice
import random
import time

class Motherboard:
        
        def __init__(self):
            self.sensores = []
            self.bateria = 100
            self.messageId = 0
            self.deviceId = 'DeviceId'
            self.registry = iotDevice.IoTHubDeviceClient.create_from_connection_string('DevicePrimaryConnectionString')
            self.registry.connect()
            
        def addSensor(self, sensor):
            self.sensores.append(sensor)
            
        def simulate(self):
            listData = []
            listIdSensor = []
            for sensor in self.sensores:
                sensor.generateValue()
                sensor.sendValueDb()
                listData.append(sensor.valor)
                listIdSensor.append(sensor.idSensor)
                
            self.messageId += 1
                
            message = {
                'messageId': self.messageId,
                'vehicleId': self.sensores[0].fkVeiculo,
                'sensorId': listIdSensor,
                'registry': listData,
                'battery': self.bateria
            }
            
            jsonMessage = json.dumps(message)
            
            print(f'Mensagen: {jsonMessage}')
            print(f'Bytes Mensagem: {sys.getsizeof(jsonMessage)}')
            
            if sys.getsizeof(jsonMessage) <= 200:
                
                chanceErro = random.randint(1, 100)
                
                if chanceErro <= 3:
                    print('Erro ao enviar mensagem!')
                else:
                    try:
                        self.registry.send_message(jsonMessage)
                    except Exception as e:
                        print(f'Erro ao enviar mensagem: {e}')
                
                self.bateria -= 0.05
            else:
                print(f'Mensagem maior que 200 bytes!\nTamanho da mensagem: {sys.getsizeof(jsonMessage)}')
                
        def run(self):
            while True:
                self.simulate()
                
                time.sleep(60)
                
        def economicRun(self):
            while True:
                listData = []
                listIdSensor = []
                for x in self.sensores:
                    x.generateValue()
                    x.sendValueDb()
                    listData.append(x.valor)
                    listIdSensor.append(x.idSensor)
                    
                    
                self.messageId += 1
                
                message = {
                    'm': self.messageId,
                    'v': self.sensores[0].fkVeiculo,
                    's': listIdSensor,
                    'r': listData,
                    'b': self.bateria
                }
                
                jsonMessage = json.dumps(message)
                
                print(f'Mensagen: {jsonMessage}')
                print(f'Bytes Mensagem: {sys.getsizeof(jsonMessage)}\n')
                
                msgCompressed = self.compress(jsonMessage)
                
                print(f'Mensagem Comprimida: {msgCompressed}')
                print(f'Bytes Mensagem Comprimida: {sys.getsizeof(msgCompressed)}\n')
                
                msgDecompressed = self.descompress(msgCompressed)
                
                print(f'Mensagem Descomprimida: {msgDecompressed}')
                print(f'Bytes Mensagem Descomprimida: {sys.getsizeof(msgDecompressed)}\n')
                
                
                time.sleep(10)