# Data Generation Algorithm/Pseudocode

## Approach

The overall approach to the data generation was to utilize the structures of the SmartHome python object in conjunction with the Simulation python object to create a realistic representation of data based on the idea of four real people living in the home. 

### SmartHome object explained
The SmartHome object was designed as a representation of an object-oriented Smart Home hub. The object contains within its state all of the components (sensors, appliances, etc.) as objects with their own state and functionality (engage()/disengage(), engaged, wattage, etc.).

The SmartHome also contains a database connection in its state that is passed to all components upon creation so the components can communicate events directly to the database.

### Simulation object explained
At its core, the simulation object exists mainly to simulate the real-world conditions of our virtual SmartHome. It has state to keep up with current exterior temp, weather, datetime, temperature delta within the house, etc. 

It accomplishes this by accepting a SmartHome object in its constructor and storing it as state. When things change within the simulation, it can reference SmartHome state and the state of all Components directly through that reference.

Considering what the Simulation does, I figured we could get a good data generation paradigm by actually running through the 60 days of required data second-by-second and alter the state of the SmartHome appropriately based on the historic temperature data, what devices were active/needed to activate, etc.

In order to interact with the SmartHome and its Components in a meaningful way, I decided to create a Person object that could "move" about the house, interact with Components, and "sleep"/"go to work or school."

### Person object explained
The Person object has state that defines its actions within the Simulation, such as assigned bedroom/bathroom, daily schedule, and adult/child status. Also contained in the Person object are functions for interacting with Components in the SmartHome. These interactions can be "occupying" or not. If a task is occupying, that means the Person interacting with the Component cannot participate in any other actions until that interaction is scripted to end. If a task is not occupying (such as starting the dishwasher), the Person will still be available to do other tasks and the Component will be set to disengage() sometime later in the day by adding the task to the Simulation's auto-resolve task list.

Tasks are assigned to a Person at midnight each day based on a pseudo-random generation found in the *schedule_builder.py* file. During the times of sleep and school/work, a Person becomes unavailable to participate in any tasks.

### A day in the life of a poor, imaginary Person person...
During data generation mode, at each midnight, a Person has the state updated with the results of a schedule chosen from the *schedule_builder.py* file based on the day of the week, if they are an adult or child, and randomly between two possible schedules for the adult/child status. Each task in the schedule is stored as a tuple with the form (task_datetime, function_name, function_params). As the simulation time ticks second-by-second, at each tick, each Person's schedule is checked to see if any actions should happen at the current time--if an action should happen, the function stored at index 1 is called by unpacking the params at index 2.

If no task needs to be done/is being done by the Person, there is a 1/1000 chance they will decide to move to another room in the house based on what rooms are logical for them to visit (their rooms and common rooms). Whenever a Person exits a room, if no other Person is in the room, all lights/fans in the room will be turned off (aren't they energy-concious little non-humans?). Upon entering a room, if there is no character in the room, all lights/fans will be turned on. There is also a 1/2000 chance a Person will open windows in their current room (if windows are there). These windows will stay open for a random time between 5-60 minutes and close on their own (it would have been difficult to ensure a Person shutting the window itself would be available to complete the task so I hand-waved that aspect).

# Pseudocode

### Handle tasks
```
def resolve_tasks():
    for each resident:
        if current_time == current_task_time:
            occupying_component.disengage()
            current_task_time = null
            occupied = false
        for each event in schedule:
            if event_time == current_time:
                execute_task()
    for each task in auto_resolve:
        if current_time == task_time:
            task_component.disengage()
            remove task from auto_resolve
```

### Handle random events
```
def random_move():
    if randint(0, 1000) == 0:
        resident = random(residents)
        if resident not occupied:
            move_to(random(rooms))

def random_window():
    if randint(0, 2000) == 0:
        resident = random(residents)
        if resident not occupied:
            open_windows()

def handle_random_events():
    random_move()
    random_window()
```

### Handle simulation environment
```
def update_temp_delta():
    temp_diff = exterior_temp - interior_temp
    temp_delta = temp_diff * (0.2/3600)
    for each door.engaged:
        temp_delta += temp_diff * (0.2/300)
    for each window.engaged:
        temp_delta += temp_diff * (0.1/300)
    if hvac.engaged and cooling:
        temp_delta -= 1/60
    if hvac.engaged and heating:
        temp_delta += 1/60
    set state temp_delta = temp_delta

def fetch_ext_temp():
    set state exterior_temp = ext_temp_map.get(current_time)

def check_thermostat():
    update_temp_delta()
    interor_temp += temp_delta
    smart_home.check_thermostat()

def check_water_heater():
    if water_to_heat > 0 and not water_heater.engaged:
        water_heater.engage()
    if water_to_heat == 0 and water_heater.engaged:
        water_heater.disengage()
    if water_heater.engaged()
        water_to_heat -= 0.25/60
```

### Handle time ticks
```
def handle_regular_tasks():
    smart_home.time = current_time
    exterior_temp = fetch_ext_temp()
    if current_time == midnight:
        build_person_schedules()
    if current_time == 20:30:
        turn off all lights/fans in house
    handle_random_events()
    resolve_tasks()
    check_thermostat()
    check_water_heater()

def build_schedules():
    for each resident:
        if resident is adult:
            random(adult_schedule)
        if resident is child:
            random(child_schedule)

def increment_second():
    handle_regular_tasks()
    current_time += 1sec
```

### Driver function
```
def simulate(number_of_days_to_generate):
    current_time = now - number_of_days_to_generate
    fetch external temps from current_time to now
    while current_time < now:
        increment_second()
```