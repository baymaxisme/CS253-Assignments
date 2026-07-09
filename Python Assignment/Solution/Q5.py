from abc import ABC
class PhysicsConstraintError(Exception):
    """Custom exception raised when a train is too heavy to move"""
    pass

class RollingStock(ABC):
    def __init__(self, id_str, weight):
        self.id_str = id_str
        self.weight = weight

class Locomotive(RollingStock):
    def __init__(self, id_str, weight, pull_capacity, fuel_rate):
        super().__init__(id_str, weight)
        self.pull_capacity = pull_capacity
        self.fuel_rate = fuel_rate

class FreightCar(RollingStock):
    def __init__(self, id_str, empty_weight, cargo_weight, destination):
        super().__init__(id_str, empty_weight) # weight = empty_weight
        self.cargo_weight = cargo_weight
        self.destination = destination

    @property
    def total_weight(self):
        return self.weight + self.cargo_weight
    
class Train:
    def __init__(self):
        self.elements = []  #list managing all connected RollingStock objects
    
    def couple(self, stock):
        self.elements.append(stock)

    def uncouple(self, stock_id):
        for i, stock in enumerate(self.elements):
            if stock.id_str == stock_id:
                return self.elements.pop(i)
        return None
    
    def get_total_weight(self):
        total = 0.0
        for stock in self.elements:
            if isinstance(stock, FreightCar): #if stock is a freight car
                total += stock.total_weight
            else:
                total += stock.weight
        return total
    
    def get_total_pull(self):
        total_pull = 0.0
        for stock in self.elements:
            if isinstance(stock, Locomotive): #if stock is a locomotive
                total_pull += stock.pull_capacity
        return total_pull
    
    def validate_physics(self):
        if self.get_total_weight() > self.get_total_pull():
            raise PhysicsConstraintError("Overload: Total weight exceeds pull capacity.")


class RailwayNetwork:
    def __init__(self):
        self.graph = {} 
        #{Station: {Neighbor: Distance}}
    
    def add_link(self, station_A, station_B, distance):
        if station_A not in self.graph:
            self.graph[station_A] = {}
        if station_B not in self.graph:
            self.graph[station_B] = {}
        self.graph[station_A][station_B] = distance
        self.graph[station_B][station_A] = distance

    def get_distance(self, station_A, station_B):
        return self.graph.get(station_A, {}).get(station_B, -1) 
        # used .get first to see if station_A exists then to see if station_B is actually connecte to it.
    

def run_delivery_schedule(train, network, route_list):
    total_fuel_consumed = 0.0

    for i in range(len(route_list)):
        current_station = route_list[i]

        #Arrival and uncoupling 
        # We use a copy of the list [:] to avoid index errors while removing items
        for stock in train.elements[:]:
            if isinstance(stock, FreightCar) and stock.destination == current_station:
                train.uncouple(stock.id_str)

        if i+1 < len(route_list):
            next_station = route_list[i+1]

            #Physics check
            train.validate_physics()
            
            #Fuel calculation
            #Get the average fuel rate of all current locomotives
            locos = [stock for stock in train.elements if isinstance(stock, Locomotive)]
            if not locos:
                raise PhysicsConstraintError("No locomotives attached to move the train")
            
            avg_fuel_rate = sum(l.fuel_rate for l in locos) / len(locos)

            #Get distance from the network
            distance = network.get_distance(current_station, next_station)
            if distance == -1:
                raise ValueError("No track exists between {} and {}".format(current_station, next_station))
            
            #Trip fuel = Total Weight * Distance * Avg Fuel Rate
            trip_fuel = train.get_total_weight()*distance*avg_fuel_rate
            total_fuel_consumed += trip_fuel

    return total_fuel_consumed

#SAMPLE
#if __name__ == "__main__":
#    net = RailwayNetwork()
#    net.add_link("Delhi", "Kanpur", 400)
#    net.add_link("Kanpur", "Prayagraj", 200)
#
#    train = Train()
#    train.couple(Locomotive("L1", weight=100, pull_capacity=500, fuel_rate=0.01))
#
#    train.couple(FreightCar("C1", empty_weight=20, cargo_weight=80, destination="Kanpur"))
#    train.couple(FreightCar("C2", empty_weight=20, cargo_weight=180, destination="Prayagraj"))
#
#    total_fuel = run_delivery_schedule(
#        train,
#        net,
#        ["Delhi", "Kanpur", "Prayagraj"]
#   )
#
#    print(total_fuel)