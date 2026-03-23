from datetime import datetime
import openmeteo_requests

class IncreaseSpeed():
    '''
  Iterator for increasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h
    max_speed: a maximum possible value, km/h
    step: a parameter to vary the value to increase by

  Make sure your iterator is not exceeding the maximum allowed value
    '''

    def __init__(self, current_speed: int, max_speed: int, step=10):
        self.current_speed = current_speed
        self.max_speed = max_speed
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        # если уже достигли или превысили максимум — стоп
        if self.current_speed >= self.max_speed:
            raise StopIteration


        self.current_speed += self.step

        if self.current_speed > self.max_speed:
            self.current_speed = self.max_speed

        return self.current_speed
     

class DecreaseSpeed():
    '''
  Iterator for decreasing the speed with the default step of 10 km/h
  You can implement this one after Iterators FP topic

  Constructor params:
    current_speed: a value to start with, km/h

  Make sure your iterator is not going below zero
    '''

    def __init__(self, current_speed: int, min_speed: int = 0, step=10):
        self.current_speed = current_speed
        self.min_speed = min_speed
        self.step = step

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_speed <= self.min_speed:
            raise StopIteration

        self.current_speed -= self.step


        if self.current_speed < self.min_speed:
            self.current_speed = self.min_speed

        return self.current_speed

class Car():
    '''
      Car class.
      Has a class variable for counting total amount of cars on the road (increased by 1 upon instance initialization).
    
      Constructor params:
        max_speed: a maximum possible speed, km/h
        current_speed: current speed, km/h (0 by default)
        state: reflects if the Car is in the parking or on the road
    
      Methods:
        accelerate: increases the speed using IncreaseSpeed() iterator either once or gradually to the upper_border
        brake: decreases the speed using DecreaseSpeed() iterator either once or gradually to the lower_border
        parking: if the Car is not already in the parking, removes the Car from the road
        total_cars: show the total amount of cars on the road
        show_weather: shows the current weather conditions
    '''
    cars_on_road = 0
    def __init__(self, max_speed: int, current_speed=0):
        self.max_speed = max_speed
        self.current_speed = current_speed
        if current_speed > 0:
            self.state = True
        else:
            self.state = False
        if self.state:
            Car.cars_on_road += 1

    def accelerate(self, upper_border=None, step=10):
    # check for state
    # create an instance of IncreaseSpeed iterator
    # check if smth passed to upper_border and if it is valid speed value
    # if True, increase the speed gradually iterating over your increaser until upper_border is met
    # print a message at each speed increase
    # else increase the speed once
    # return the message with current speed
        if not self.state:
            self.state = True
            Car.cars_on_road += 1

        start_speed = self.current_speed

        if upper_border is None:
            upper_border = min(self.current_speed + step, self.max_speed)
        else:
            upper_border = min(upper_border, self.max_speed)

        increaser = IncreaseSpeed(self.current_speed, upper_border, step)

        for new_speed in increaser:
            diff = new_speed - self.current_speed
            print(f">> INFO: Speed increases by {diff}")
            self.current_speed = new_speed

            if self.current_speed >= upper_border:
                break

        print(f">> INFO: The speed of this car has been increased from {start_speed} to {self.current_speed}")
      
    def brake(self, lower_border=None, step=10):

        
        start_speed = self.current_speed

        if lower_border is None:
            lower_border = max(self.current_speed - step, 0)
        else:
            lower_border = max(lower_border, 0)

        decreaser = DecreaseSpeed(self.current_speed, lower_border, step)

        for new_speed in decreaser:
            diff = self.current_speed - new_speed
            print(f">> INFO: Speed decreases by {diff}")
            self.current_speed = new_speed

            if self.current_speed <= lower_border:
                break

        print(f">> INFO: The speed of this car has been decreased from {start_speed} to {self.current_speed}")

  # the next three functions you have to define yourself
  # one of the is class method, one - static and one - regular method (not necessarily in this order, it's for you to think)

    def parking(self):
        if not self.state:
            print("Car is already in parking")
            return

        self.brake(0)

        print("Parking the car...")

        self.state = False
        Car.cars_on_road -= 1
  
      
    # gets car off the road (use state and class variable)
    # check: should not be able to move the car off the road if it's not there


    @classmethod 
    def total_cars(cls):
    # displays total amount of cars on the road
        return cls.cars_on_road
      
    @staticmethod
    def show_weather():
        openmeteo = openmeteo_requests.Client()
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
        "latitude": 59.9386, # for St.Petersburg
        "longitude": 30.3141, # for St.Petersburg
        "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
        "wind_speed_unit": "ms",
        "timezone": "Europe/Moscow"
        }

        response = openmeteo.weather_api(url, params=params)[0]

        # The order of variables needs to be the same as requested in params->current!
        current = response.Current()
        current_temperature_2m = current.Variables(0).Value()
        current_apparent_temperature = current.Variables(1).Value()
        current_rain = current.Variables(2).Value()
        current_wind_speed_10m = current.Variables(3).Value()

        print(f"Current time: {datetime.fromtimestamp(current.Time()+response.UtcOffsetSeconds())} {response.TimezoneAbbreviation().decode()}")
        print(f"Current temperature: {round(current_temperature_2m, 0)} C")
        print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
        print(f"Current rain: {current_rain} mm")
        print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")

car1 = Car(100, 20) # max_speed = 100, initial speed = 5
car2 = Car(60, 30) # max_speed = 60, initial speed = 30
car3 = Car(100, 0) # a car that is off road upon creation
print(f"Total cars on road: {Car.total_cars()}")
car1.accelerate(100)

car2.accelerate(50)
print("Speed of car 1:", car1.current_speed)
print("Speed of car 2:", car2.current_speed)
 
car1.brake(10)
car2.brake(0)
car2.parking()
print("Total cars on road:", Car.total_cars())
car3.accelerate(80)# car3 is now on the road
car3.show_weather()
print("Total cars on road:", Car.total_cars())
car2.accelerate(10) # # car2 goes from parking on the road
print("Total cars on road:", Car.total_cars())

Car.show_weather()