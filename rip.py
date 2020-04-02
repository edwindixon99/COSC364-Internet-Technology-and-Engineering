import sys
import socket

HOST = "127.0.0.1"



class Demon:
    def __init__(self, id, inputs, outputs, timer=None):
        self.id = id
        self.inputs = inputs
        self.outputs = outputs
        self.timer = timer

    def __repr__(self):
        return "router" + str(self.id)

class Outport_Port:
    def __init__(self, port, metric, peer_id):
        self.port = port
        self.metric = metric
        self.peer_id = peer_id

    def __repr__(self):
        return "{}".format((self.port, self.metric, self.peer_id))

#----------------------------------------------------------  
def get_inputs(line, output=0):           #set output to 1 for the outputs config line
    inputs = line.split(' ')[1:]
    
    for i in range(len(inputs)):

        inputs[i] = inputs[i].strip(",")
        if output == 1:                                
            inputs[i] = get_output_input(inputs[i])
        else:
            inputs[i] = int(inputs[i])

    return inputs
    
def get_output_input(data):
    data = data.split('-')
    
    for i in range(len(data)):
        data[i] = int(data[i])
    return Outport_Port(data[0], data[1], data[2])
#----------------------------------------------------------    
# Validation checks (not complete)
def valid_config(router_id, demons, input_ports, output_ports):
    return unique_valid_id(router_id, demons) and valid_ports(input_ports, output_ports)

def unique_valid_id(router_id, demons):
    if router_id <= 0:
        return False
    for demon in demons:
        if demon.id == router_id:
            return False 
    return True


def valid_ports(input_ports, output_ports):
    for port in input_ports:
        if not (1024 <= port <= 64000):
            return False
    for port in output_ports:
        if not (1024 <= port.port <= 64000):
            return False
        if port.port in input_ports:          # input port cannot be an output port
            return False
        #if not (0 <= port.metric <= 15):           # metric bounds between 0 and ?(not sure) 
            #return False
        # Other checks
    return True

#---------------------------------------------------------------------------------------------------------  


def get_demon(configs, demons):
    for i in range(len(configs)):
        configs[i] = configs[i].rstrip()
    #print(configs[i])
        if configs[i].startswith("router-id:"):
            router_id = get_inputs(configs[i])[0]
            #print(router_id)
        elif configs[i].startswith("input-ports:"):
            input_ports = get_inputs(configs[i])
            #print(input_ports)
        elif configs[i].startswith("outputs:"):
            output_ports = get_inputs(configs[i], 1)
            #print(output_ports)
        elif configs[i].startswith("update:"):
            update = get_inputs(configs[i])[0]
            #print(update)

    print("loaded values")
    print(router_id, input_ports,output_ports,update)
    print("")
    if valid_config(router_id, demons, input_ports, output_ports):
        return Demon(router_id, input_ports, output_ports)
    
def readconf():
    print("\n******trying to open file******\n")
    file = open("./Config/" + sys.argv[1], "r")

    configs = file.readlines()

    for x in configs:
        print(x)

    print("********************************\n")

    demons = []
    demon = get_demon(configs, demons)
    if demon is not None:
        demons.append(demon)

    return demons
    
        

def inputSockets(deamon):
    socket_values = deamon.inputs
    sockets = []
    print("")
    print("Starting socket construction.\n")
    for value in socket_values:
        print("Building socket " + str(value))
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.bind((HOST, value))
        sockets.append(sock)

    print("\nsocket construction done.\n" + str(len(sockets)) + " scokets have been made.")
    return sockets



def main():
    print("starting rip")

    if (len(sys.argv) < 2):
        print("no config file")
        sys.exit()

    demons = readconf()

    for demon in demons:
        ##print(demon)
        print(demon.id, demon.inputs, demon.outputs)

    sockets = inputSockets(demons[0])
    


if __name__ == "__main__":
    main()