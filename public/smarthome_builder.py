## Define household components and connect them to the database
def build_home(db_conn):
    return {
        "lights": [
            (db_conn, "light_01", "Bedroom_1 Overhead", 60),
            (db_conn, "light_02", "Bedroom_2 Overhead", 60),
            (db_conn, "light_03", "Bedroom_3 Overhead", 60),
            (db_conn, "light_04", "Bedroom_1 Lamp 1", 60),
            (db_conn, "light_05", "Bedroom_1 Lamp 2", 60),
            (db_conn, "light_06", "Bedroom_2 Lamp 1", 60),
            (db_conn, "light_07", "Bedroom_2 Lamp 2", 60),
            (db_conn, "light_08", "Bedroom_3 Lamp 1", 60),
            (db_conn, "light_09", "Bedroom_3 Lamp 2", 60),
            (db_conn, "light_10", "Bathroom_1 Overhead", 60),
            (db_conn, "light_11", "Bathroom_2 Overhead", 60),
            (db_conn, "light_12", "Living_Room Overhead", 60),
            (db_conn, "light_13", "Living_Room Lamp 1", 60),
            (db_conn, "light_14", "Living_Room Lamp 2", 60),
            (db_conn, "light_15", "Kitchen Overhead", 60),
        ],
        "appliances": [
            (db_conn, "tv_01", "Bedroom_1 TV", 100),
            (db_conn, "tv_02", "Living_Room TV", 636),
            (db_conn, "fan_01", "Bathroom_1 Fan", 30),
            (db_conn, "fan_02", "Bathroom_2 Fan", 30),
            (db_conn, "hvac_01", "HVAC", 3500),
            (db_conn, "ref_01", "Refrigerator", 150),
            (db_conn, "water-heater_01", "Hot Water Heater", 4500),
            (db_conn, "microwave_01", "Microwave", 1100),
            (db_conn, "stove_01", "Stove", 3500),
            (db_conn, "oven_01", "Oven", 4000),
            (db_conn, "dishwasher_01", "Dishwasher", 1800),
            (db_conn, "clothes-washer_01", "Clothes Washer", 500),
            (db_conn, "clothes-dryer_01", "Clothes Dryer", 3000)
        ],
        "baths": [
            (db_conn, "bath_01", "Bathroom_1 Bath"),
            (db_conn, "bath_02", "Bathroom_2 Bath")
        ],
        "ext_doors": [
            (db_conn, "door_01", "Front Door"),
            (db_conn, "door_02", "Back Door"),
            (db_conn, "door_03", "House to Garage Door"),
        ],
        "other_doors": [
            (db_conn, "garage_01", "Garage Door 1"),
            (db_conn, "garage_02", "Garage Door 2"),
        ],
        "windows": [
            (db_conn, "window_01", "Bedroom_1 Window 1"),
            (db_conn, "window_02", "Bedroom_1 Window 2"),
            (db_conn, "window_03", "Bedroom_2 Window 1"),
            (db_conn, "window_04", "Bedroom_1 Window 2"),
            (db_conn, "window_05", "Bedroom_3 Window 1"),
            (db_conn, "window_06", "Bedroom_3 Window 2"),
            (db_conn, "window_07", "Bathroom_1 Window 1"),
            (db_conn, "window_08", "Bathroom_2 Window 1"),
            (db_conn, "window_09", "Living_Room Window 1"),
            (db_conn, "window_10", "Living_Room Window 2"),
            (db_conn, "window_11", "Living_Room Window 3"),
            (db_conn, "window_12", "Kitchen Window 1"),
            (db_conn, "window_13", "Kitchen Window 2")
        ]
    }