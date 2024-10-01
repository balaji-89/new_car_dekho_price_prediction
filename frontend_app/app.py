import streamlit as st
import pandas as pd
import pickle 
import dill
from load_preprocess_data.preprocess_pipeline import *



# Title
st.title("Second-Hand Car Price Prediction")

# Section 1: Basic Car Information
st.header("Basic Information")

# First row: Transmission, Owner No, OEM, Model
col1, col2, col3, col4 = st.columns(4)
transmission = col1.selectbox("Transmission", ['Manual', 'Automatic'])
ownerno = col2.number_input("Total no of previous owners",min_value = 1,max_value = 10)







original_equipment_manufacturer = col3.selectbox("Manufactured Company",
        ['Kia', 'Hyundai', 'Mercedes-Benz', 'Maruti', 'Volkswagen', 'Honda',
       'Nissan', 'Toyota', 'BMW', 'Mini', 'MG', 'Tata', 'Skoda',
       'Mahindra', 'Isuzu', 'Audi', 'Fiat', 'Renault', 'Jeep', 'Datsun',
       'Ford', 'Mitsubishi', 'Land Rover', 'Lexus', 'Volvo', 'Porsche',
       'Jaguar', 'Chevrolet', 'Hindustan Motors', 'Mahindra Ssangyong',
       'Mahindra Renault', 'Citroen', 'Opel'])

model = col4.selectbox("Model",
        ['Kia Seltos', 'Hyundai Creta', 'Mercedes-Benz GLC', 'Maruti Swift',
       'Kia Sonet', 'Hyundai Aura', 'Volkswagen Polo',
       'Hyundai Grand i10 Nios', 'Maruti Baleno', 'Honda Brio',
       'Nissan Kicks', 'Toyota Camry', 'BMW 5 Series', 'Mini Cooper SE',
       'Toyota Innova Crysta', 'MG Gloster', 'BMW X1',
       'Tata Safari Storme', 'Hyundai Venue', 'Maruti Zen Estilo',
       'Skoda Kushaq', 'Tata Altroz', 'Maruti Ignis', 'BMW 7 Series',
       'BMW 3 Series GT', 'Hyundai Grand i10', 'Mahindra XUV500',
       'MG Hector Plus', 'Honda Amaze', 'Hyundai i10',
       'Toyota Corolla Altis', 'Toyota Etios', 'Maruti Wagon R',
       'Isuzu MU-X', 'Maruti Swift Dzire', 'Mahindra Scorpio',
       'Honda Jazz', 'Maruti Brezza', 'Tata Tiago', 'Audi A6',
       'Hyundai Santro', 'Maruti Celerio', 'Mercedes-Benz S-Class',
       'Fiat Linea', 'Nissan Terrano', 'Renault KWID', 'Honda City',
       'Audi Q5', 'BMW X5', 'Hyundai i20', 'Mercedes-Benz E-Class',
       'Maruti Ertiga', 'Toyota Glanza', 'Jeep Compass', 'Renault Triber',
       'Maruti Vitara Brezza', 'Jeep Wrangler', 'Hyundai Elantra',
       'Mahindra Scorpio N', 'Datsun RediGO', 'Hyundai Xcent',
       'Tata Tigor', 'Ford Ecosport', 'Hyundai EON', 'Mahindra Thar',
       'Mercedes-Benz GLA Class', 'Maruti A-Star', 'Mitsubishi Pajero',
       'Mahindra XUV700', 'Toyota Etios Cross', 'Volkswagen Vento',
       'Audi A4', 'BMW X4', 'Land Rover Defender', 'Tata Nexon',
       'Honda WR-V', 'Toyota Etios Liva', 'Mercedes-Benz GLC Coupe',
       'Maruti Celerio X', 'Maruti Wagon R Stingray', 'Lexus RX',
       'Hyundai Verna', 'Audi A3', 'Mitsubishi Outlander',
       'Mercedes-Benz CLA', 'Kia Carnival', 'Skoda Rapid',
       'Maruti Alto 800', 'Land Rover Range Rover Sport',
       'Tata Indica V2', 'Skoda Octavia', 'Mercedes-Benz GLS',
       'Toyota Fortuner', 'Audi Q7', 'BMW 6 Series', 'Maruti Ciaz',
       'Mercedes-Benz M-Class', 'Tata Harrier', 'Mercedes-Benz CLS-Class',
       'Maruti Jimny', 'Volvo XC60', 'Mini Cooper Clubman',
       'Land Rover Discovery', 'Mercedes-Benz GLE', 'Ford Aspire',
       'Land Rover Discovery Sport', 'Mercedes-Benz C-Class', 'Ford Figo',
       'MG Astor', 'Ford Endeavour', 'Land Rover Range Rover Evoque',
       'Mercedes-Benz AMG A 35', 'Porsche Cayenne', 'Audi Q3',
       'Mercedes-Benz AMG G 63', 'Volkswagen Ameo', 'Tata New Safari',
       'BMW X7', 'Renault Duster', 'Audi Q3 Sportback', 'Audi Q2',
       'Maruti Swift Dzire Tour', 'Volvo XC40', 'Hyundai i20 Active',
       'Maruti Alto K10', 'Maruti S-Presso', 'Mercedes-Benz GLA',
       'Honda CR-V', 'Porsche Macan', 'Mercedes-Benz G',
       'Mini Cooper Convertible', 'Volvo XC 90', 'Nissan Magnite',
       'Tata Hexa', 'Maruti SX4 S Cross', 'BMW 3 Series Gran Limousine',
       'MG Hector', 'Tata Punch', 'Mahindra KUV 100', 'Skoda Fabia',
       'Mini Cooper', 'Renault Kiger', 'Toyota Vellfire',
       'Mahindra Bolero Power Plus', 'Mahindra XUV300', 'BMW 3 Series',
       'Hyundai Accent', 'Toyota Land Cruiser 300',
       'Toyota Fortuner Legender', 'Jaguar XF', 'Nissan Micra',
       'Jaguar F-Pace', 'Mahindra Scorpio Classic', 'Jaguar XE',
       'Hyundai Tucson', 'Tata Zest', 'Volkswagen Jetta', 'Volvo S90',
       'Maruti XL6', 'Toyota Urban cruiser', 'Skoda Superb',
       'Mercedes-Benz SLC', 'Mercedes-Benz A-Class Limousine',
       'Chevrolet Beat', 'Maruti Ritz', 'Ford Freestyle',
       'Datsun GO Plus', 'Skoda Slavia', 'Mahindra KUV 100 NXT',
       'Volkswagen Taigun', 'Chevrolet Spark', 'Maruti Alto',
       'Isuzu D-Max', 'Maruti Grand Vitara', 'Hyundai Santro Xing',
       'Honda Civic', 'Toyota Yaris', 'Nissan Sunny', 'Chevrolet Optra',
       'Hyundai Alcazar', 'Mahindra TUV 300', 'Honda Mobilio',
       'Tata Manza', 'Toyota Hyryder', 'Mini Cooper Countryman',
       'Mercedes-Benz GL-Class', 'Tata Nexon EV Prime', 'Fiat Punto',
       'Mercedes-Benz A Class', 'Toyota Innova', 'Maruti SX4',
       'Ford Fiesta Classic', 'Maruti FRONX', 'Hyundai i20 N Line',
       'Maruti Celerio Tour 2018-2021', 'Lexus ES', 'Jaguar XJ',
       'Mahindra Alturas G4', 'Maruti 800', 'Mahindra Bolero',
       'Mahindra Marazzo', 'Honda BR-V', 'Ambassador', 'Skoda Laura',
       'Volvo S60 Cross Country', 'Chevrolet Tavera',
       'Jeep Compass Trailhawk', 'Land Rover Range Rover Velar',
       'Renault Scala', 'Tata Sumo Victa', 'BMW X3', 'Renault Captur',
       'Chevrolet Sail', 'Honda New Accord', 'Nissan Micra Active',
       'Volvo V40', 'Porsche Panamera', 'Hyundai Sonata',
       'Mercedes-Benz AMG GT', 'Datsun GO', 'Tata Indica', 'Tata Indigo',
       'Land Rover Freelander 2', 'Maruti Estilo', 'Audi S5 Sportback',
       'Chevrolet Aveo', 'Renault Pulse', 'Mahindra Ssangyong Rexton',
       'Maruti Zen', 'Ford Fiesta', 'Mahindra Renault Logan',
       'Tata Tiago NRG', 'Kia Carens', 'Mahindra Bolero Neo',
       'Jeep Meridian', 'Chevrolet Cruze', 'Tata Nexon EV', 'Maruti Eeco',
       'Jaguar F-TYPE', 'Tata Tigor EV', 'Mahindra Xylo',
       'Fiat Grande Punto', 'Hyundai Xcent Prime', 'Skoda Kodiaq',
       'Tata Nano', 'Mercedes-Benz AMG GLC 43', 'Chevrolet Aveo U-VA',
       'Hyundai Kona', 'Tata Nexon EV Max', 'MG ZS EV', 'Hyundai Getz',
       'Hyundai Santa Fe', 'Mahindra Bolero Camper', 'Maruti Omni',
       'Maruti Esteem', 'Citroen C3', 'Porsche 911', 'Maruti Baleno RS',
       'Mahindra Quanto', 'Fiat Avventura', 'Volkswagen Passat',
       'Volkswagen CrossPolo', 'Fiat Punto EVO', 'Volvo S60',
       'Mahindra Jeep', 'Toyota Qualis', 'Citroen C5 Aircross',
       'Maruti Gypsy', 'Chevrolet Enjoy', 'BMW 1 Series',
       'Volkswagen Virtus', 'Land Rover Range Rover', 'Honda City Hybrid',
       'Tata Aria', 'Tata Bolt', 'Mahindra E Verito', 'Mercedes-Benz EQC',
       'Fiat Abarth Avventura', 'Hindustan Motors Contessa',
       'Tata Yodha Pickup', 'Tata Indigo Marina', 'Chevrolet Captiva',
       'Mahindra Bolero Pik Up Extra Long', 'Ford Ikon',
       'Mercedes-Benz B Class', 'Toyota Corolla', 'Maruti Ertiga Tour',
       'Isuzu MU 7', 'Renault Fluence', 'Ford Mondeo', 'Mitsubishi Cedia',
       'BMW 2 Series', 'Mini 5 DOOR', 'Maruti Versa', 'Mitsubishi Lancer',
       'Fiat Punto Pure', 'Volvo S 80', 'Skoda Yeti', 'Audi A8',
       'Mercedes-Benz AMG GLA 35', 'Mahindra TUV 300 Plus',
       'Volkswagen Tiguan', 'Mini 3 DOOR', 'Renault Lodgy',
       'Volkswagen T-Roc', 'Mahindra Verito', 'Mahindra e2o Plus',
       'MG Comet EV', 'Fiat Punto Abarth', 'Maruti 1000', 'OpelCorsa',
       'Volkswagen Tiguan Allspace', 'Tata Sumo', 'Fiat Palio',
       'Audi A3 cabriolet'])

# Section 2: Performance & Features
st.header("Performance & Features")

# Create a grid of columns for this section
cols = st.columns(4)
drive_modes = cols[0].selectbox("Drive Modes",['Yes', 'No'])
voice_control = cols[1].selectbox("Voice Control", ['Yes', 'No'])
smart_key_band = cols[2].selectbox("Smart Key Band", ['Yes', 'No'])
battery_saver = cols[3].selectbox("Battery Saver", ['Yes', 'No'])

# Additional performance features
rear_reading_lamp = cols[0].selectbox("Rear Reading Lamp", ['Yes', 'No'])
power_boot = cols[1].selectbox("Power Boot", ['Yes', 'No'])
power_steering = cols[2].selectbox("Power Steering", ['Yes', 'No'])
real_time_vehicle_tracking = cols[3].selectbox("Real-time Vehicle Tracking", ['Yes', 'No'])

luggage_hook_and_net = cols[0].selectbox("Luggage Hook & Net", ['Yes', 'No'])
cruise_control = cols[1].selectbox("Cruise Control", ['Yes', 'No'])
seat_lumbar_support = cols[2].selectbox("Seat Lumbar Support", ['Yes', 'No'])
power_windows_front = cols[3].selectbox("Power Windows Front", ['Yes', 'No'])

# Section 3: Comfort & Interior
st.header("Comfort & Interior")

# Split into multiple rows to display more fields
col1, col2, col3, col4 = st.columns(4)

vanity_mirror = col1.selectbox("Vanity Mirror", ['Yes', 'No'])
gear_shift_indicator = col2.selectbox("Gear Shift Indicator", ['Yes', 'No'])
trunk_light = col3.selectbox("Trunk Light", ['Yes', 'No'])
adjustable_headrest = col4.selectbox("Adjustable Headrest", ['Yes', 'No'])

engine_start_stop_button = col1.selectbox("Engine Start/Stop Button", ['Yes', 'No'])
find_my_car_location = col2.selectbox("Find My Car Location", ['Yes', 'No'])
multifunction_steering_wheel = col3.selectbox("Multifunction Steering Wheel", ['Yes', 'No'])
remote_engine_start_stop = col4.selectbox("Remote Engine Start/Stop", ['Yes', 'No'])

active_noise_cancellation = col1.selectbox("Active Noise Cancellation", ['Yes', 'No'])
remote_fuel_lid_opener = col2.selectbox("Remote Fuel Lid Opener", ['Yes', 'No'])
hands_free_tailgate = col3.selectbox("Hands-Free Tailgate", ['Yes', 'No'])
remote_trunk_opener = col4.selectbox("Remote Trunk Opener", ['Yes', 'No'])

lane_change_indicator = col1.selectbox("Lane Change Indicator", ['Yes', 'No'])
glove_box_cooling = col2.selectbox("Glove Box Cooling", ['Yes', 'No'])
tailgate_ajar = col3.selectbox("Tailgate Ajar", ['Yes', 'No'])
steering_wheel_gearshift_paddles = col4.selectbox("Steering Wheel Gearshift Paddles", ['Yes', 'No'])

rear_seat_centre_arm_rest = col1.selectbox("Rear Seat Centre Arm Rest", ['Yes', 'No'])
navigation_system = col2.selectbox("Navigation System", ['Yes', 'No'])
cup_holders_rear = col3.selectbox("Cup Holders Rear", ['Yes', 'No'])
smart_access_card_entry = col4.selectbox("Smart Access Card Entry", ['Yes', 'No'])

power_windows_rear = col1.selectbox("Power Windows Rear", ['Yes', 'No'])
cup_holders_front = col2.selectbox("Cup Holders Front", ['Yes', 'No'])
rear_acvents = col3.selectbox("Rear AC Vents", ['Yes', 'No'])
air_quality_control = col4.selectbox("Air Quality Control", ['Yes', 'No'])

low_fuel_warning_light = col1.selectbox("Low Fuel Warning Light", ['Yes', 'No'])
remote_climate_control = col2.selectbox("Remote Climate Control", ['Yes', 'No'])
power_folding3rd_row_seat = col3.selectbox("Power Folding 3rd Row Seat", ['Yes', 'No'])
steering_mounted_tripmeter = col4.selectbox("Steering Mounted Tripmeter", ['Yes', 'No'])

accessory_power_outlet = col1.selectbox("Accessory Power Outlet", ['Yes', 'No'])
rear_seat_headrest = col2.selectbox("Rear Seat Headrest", ['Yes', 'No'])
remote_horn_light_control = col3.selectbox("Remote Horn & Light Control", ['Yes', 'No'])
height_adjustable_front_seat_belts = col4.selectbox("Height Adjustable Front Seat Belts", ['Yes', 'No'])

# Section 4: Exterior Features
st.header("Exterior Features")

cols = st.columns(4)
leather_steering_wheel = cols[0].selectbox("Leather Steering Wheel", ['Yes', 'No'])
fabric_upholstery = cols[1].selectbox("Fabric Upholstery", ['Yes', 'No'])
glove_compartment = cols[2].selectbox("Glove Compartment", ['Yes', 'No'])
adjustable_steering = cols[3].selectbox("Adjustable Steering", ['Yes', 'No'])

height_adjustable_driver_seat = cols[0].selectbox("Height Adjustable Driver Seat", ['Yes', 'No'])
air_conditioner = cols[1].selectbox("Air Conditioner", ['Yes', 'No'])
cigarette_lighter = cols[2].selectbox("Cigarette Lighter", ['Yes', 'No'])
dual_tone_dashboard = cols[3].selectbox("Dual Tone Dashboard", ['Yes', 'No'])

heater = cols[0].selectbox("Heater", ['Yes', 'No'])
digital_clock = cols[1].selectbox("Digital Clock", ['Yes', 'No'])
outside_temperature_display = cols[2].selectbox("Outside Temperature Display", ['Yes', 'No'])
leather_seats = cols[3].selectbox("Leather Seats", ['Yes', 'No'])

# Section 5: Safety & Security
st.header("Safety & Security")

cols = st.columns(4)
traction_control = cols[0].selectbox("Traction Control", ['Yes', 'No'])
side_impact_beams = cols[1].selectbox("Side Impact Beams", ['Yes', 'No'])
seat_belt_warning = cols[2].selectbox("Seat Belt Warning", ['Yes', 'No'])
rear_seat_belts = cols[3].selectbox("Rear Seat Belts", ['Yes', 'No'])

power_door_locks = cols[0].selectbox("Power Door Locks", ['Yes', 'No'])
xenon_headlamps = cols[1].selectbox("Xenon Headlamps", ['Yes', 'No'])
pretensioners_and_force_limiter_seatbelts = cols[2].selectbox("Pretensioners & Force Limiter Seatbelts", ['Yes', 'No'])
side_air_bag_front = cols[3].selectbox("Side Air Bag Front", ['Yes', 'No'])

anti_lock_braking_system = cols[0].selectbox("Anti-lock Braking System", ['Yes', 'No'])
centeral_locking = cols[1].selectbox("Central Locking", ['Yes', 'No'])
hill_descent_control = cols[2].selectbox("Hill Descent Control", ['Yes', 'No'])
anti_theft_device = cols[3].selectbox("Anti-theft Device", ['Yes', 'No'])

vehicle_stability_control_system = cols[0].selectbox("Vehicle Stability Control System", ['Yes', 'No'])
blind_spot_monitor = cols[1].selectbox("Blind Spot Monitor", ['Yes', 'No'])
automatic_head_lamps = cols[2].selectbox("Automatic Head Lamps", ['Yes', 'No'])
knee_airbags = cols[3].selectbox("Knee Airbags", ['Yes', 'No'])

driver_air_bag = cols[0].selectbox("Driver air bag",['Yes','No'])
engine_immobilizer = cols[1].selectbox("Engine Immobilizer",["Yes","No"])
lane_watch_camera = cols[2].selectbox('Lane Watch Camera',['Yes','No'])
front_impact_beams = cols[3].selectbox('Front Impact Beams',['Yes','No'])

view360camera = cols[0].selectbox('View 360 Camera',['Yes','No'])
speed_sensing_auto_door_lock = cols[1].selectbox('Speed Sensing Auto Door Lock',['Yes','No'])
anti_pinch_power_windows = cols[2].selectbox('Anti pinch power windows',['Yes','No'])
speed_alert = cols[3].selectbox('Speed Alert',["Yes","No"])

hill_assist = cols[0].selectbox('Hill Assist',['Yes','No'])
passenger_side_rear_view_mirror = cols[1].selectbox('Passenger rear view mirror',['Yes','No'])
adjustable_seats = cols[2].selectbox('Adjustable Seats',['Yes','No'])
rear_camera = cols[3].selectbox('Rear Camera',["Yes","No"])

geo_fence_alert = cols[0].selectbox('Geo Fence Alert',['Yes','No'])
clutch_lock = cols[1].selectbox('Clutch Lock',['Yes','No'])
side_air_bag_rear = cols[2].selectbox('Side Air Bag Rear',['Yes','No'])
eletronic_stability_control = cols[3].selectbox('Electronic Stability Control',["Yes","No"])

child_safety_locks = cols[0].selectbox('Child Safety Locks',['Yes','No'])
ebd = cols[1].selectbox('Electronic Brakes Distribution',['Yes','No'])
centrally_mounted_fuel_tank = cols[2].selectbox('Central Mounted Fuel Tank',['Yes','No'])
crash_sensor = cols[3].selectbox('Crash Sensor',['Yes','No'])

brake_assist = cols[0].selectbox('Brake Assist',['Yes','No'])
passenger_air_bag = cols[1].selectbox('Passenger Air Bag',['Yes','No'])
sos_emergency_assistance = cols[2].selectbox('SOS Emergency Assist',['Yes','No'])
day_night_rear_view_mirror = cols[3].selectbox('Day night rear veiw mirror',['Yes','No'])

door_ajar_warning = cols[0].selectbox('Door Ajar Warning',['Yes','No'])
halogen_headlamps_1 = cols[1].selectbox('Halogen HeadLamps 1',['Yes','No'])
engine_check_warning = cols[2].selectbox('Engine Check Warning',['Yes','No'])
isofix_child_seat_mounts = cols[3].selectbox('Child Seat Mounts',['Yes','No'])

tyre_pressure_monitor = cols[0].selectbox('Tyre Pressure Monitor',['Yes','No'])
heads_up_display = cols[1].selectbox('Heads Up Display',['Yes','No'])
follow_me_home_headlamps = cols[2].selectbox('Follow me Home Headlamps',['Yes','No'])
anti_theft_alarm = cols[3].selectbox('Anti Theft Alarm',['Yes','No'])

impact_sensing_auto_door_lock = cols[0].selectbox('Impact Sensing Auto Door Lock',['Yes','No'])
keyless_entry = cols[1].selectbox('Keyless Entry',['Yes','No'])




# Section 6: Technical Specifications
st.header("Technical Specifications")

cols = st.columns(4)
color = cols[0].selectbox("Color",
        ['Gray', 'White', 'Grey', 'Silver', 'Black', 'Blue', 'Others',
       'Medium Blue', 'Red', 'Brown', 'Orange',
       'Alabaster Silver Metallic', 'Yellow', 'Golden Brown',
       'Carbon Steel', 'Cavern Grey', 'Maroon', 'Golden', 'ESPRESO_BRWN',
       'Green', 'Beige', 'Pearl White', 'Polar White', 'Magma Grey',
       'Gold', 'Purple', 'Dark Red', 'Falsa Colour', 'Cherry', 'Foliage',
       'Sky Blue', 'Off White', 'Bronze', 'G Brown', 'Parpel',
       'Outback Bronze', 'Cherry Red', 'Sunset Red', 'Silicon Silver',
       'golden brown', 'Dark Blue', 'Technometgrn+Gryroof',
       'Light Silver', 'Out Back Bronze', 'Violet', 'Bright Silver',
       'Porcelain White', 'Tafeta White', 'Coral White', 'Diamond White',
       'Brick Red', 'Carnelian Red Pearl', 'Urban Titanium Metallic',
       'Silky silver', 'Mediterranean Blue', 'Mist Silver',
       'Gravity Gray', 'Candy White', 'Metallic Premium silver',
       'Glistening Grey', 'Super white', 'Deep Black Pearl',
       'PLATINUM WHITE PEARL', 'Twilight Blue', 'Caviar Black',
       'Pearl Met. Arctic White', 'Superior white', 'Sleek Silver',
       'Phantom Black', 'Metallic silky silver', 'Pearl Arctic White',
       'Pure white', 'Smoke Grey', 'Fiery Red', 'StarDust',
       'Alabaster Silver Metallic - Amaze', 'Ray blue',
       'Glacier White Pearl', 'OUTBACK BRONZE', 'Granite Grey',
       'Solid Fire Red', 'Daytona Grey', 'Metallic Azure Grey',
       'Moonlight Silver', 'Aurora Black Pearl', 'Fire Brick Red',
       'Cashmere', 'Pearl Snow White', 'Minimal Grey',
       'Metallic Glistening Grey', 'Light Orange', 'Hip Hop Black',
       'Nexa Blue', 'Passion Red', 'Cirrus White', 'Arizona Blue',
       'Galaxy Blue', 'Silky Silver', 'Modern Steel Metal',
       'GOLDEN BROWN', 'Burgundy Red Metallic', 'magma gray', 'CBeige',
       'Goldan BRWOON', 'm grey', 'b red', 'urban titanim', 'g brown',
       'beige', 'Rosso Brunello', 'a silver', 'b grey', 'Radiant Red M',
       'c bronze', 'Champagne Mica Metallic', 'MODERN STEEL METALLIC',
       'Bold Beige Metallic', 'Starry Black', 'Symphony Silver',
       'Metallic Magma Grey','c brown', 'chill',
       'Modern Steel Metallic', 'Arctic Silver', 'TAFETA WHITE',
       'P Black', 'Golden brown', 'Star Dust', 'METALL', 'MET ECRU BEIGE',
       'COPPER', 'TITANIUM', 'CHILL', 'TITANIUM GREY', 'Burgundy',
       'Lunar Silver Metallic', 'SILKY SILVER', 'BERRY RED',
       'PREMIUM AMBER METALLIC', 'R EARTH', 'PLATINUM SILVER',
       'ORCHID WHITE PEARL', 'CARNELIAN RED PEARL', 'POLAR WHITE',
       'BEIGE', 'O Purple', 'Other', 'PLATINUM WHITE', 'Flash Red',
       'Wine Red', 'Taffeta White', 'T Wine', 'Prime Star Gaze'])


turbo_charger = cols[1].selectbox("Turbo Charger", ['Yes', 'No'])
front_brake_type = cols[2].selectbox("Front Brake Type",['Disc','Drum'])
rear_brake_type = cols[3].selectbox("Rear Brake Type",['Disc','Drum'])

kerb_weight = cols[0].number_input("Kerb Weight (kg)", min_value=0)
height = cols[1].number_input("Height (mm)", min_value=0)
wheel_base = cols[2].number_input("Wheel Base (mm)", min_value=0)
length = cols[3].number_input("Length (mm)", min_value=0)

width = cols[0].number_input("Width (mm)", min_value=0)
kilo_meter = cols[1].number_input("Kilometers Driven", min_value=0)
model_year = cols[2].number_input("Model Year", min_value=1900, max_value=2024, step=1)
engine_displacement = cols[3].number_input("Engine Displacement (cc)", min_value=0)

fuel_type = cols[0].selectbox("Fuel Type", ['Diesel', 'Petrol', 'Cng', 'Electric', 'Lpg'])
body_type = cols[1].selectbox("Body Type",
                               ['SUV', 'Hatchback', 'Sedan', 'MUV', 'Coupe', 'Convertibles', 
                                'Wagon', 'Pickup Trucks', 'Minivans', 'Hybrids'])
location = cols[2].selectbox("Location",['Delhi', 'Kolkata', 'Jaipur', 'Hyderabad', 'Chennai', 'Bangalore'])
no_of_cylinder = cols[3].number_input("No. of Cylinders", min_value=1, step=1,max_value = 12)

electronic_multi_tripmeter = cols[0].selectbox("Electronic Multi Tripmeter", ['Yes', 'No'])
rear_folding_table = cols[1].selectbox("Rear Folding Table", ['Yes', 'No'])
driving_experience_control_eco = cols[2].selectbox("Driving Experience Control (Eco)", ['Yes', 'No'])
leather_wrap_gear_shift_selector = cols[3].selectbox("Leather Wrap Gear Shift Selector", ['Yes', 'No'])

digital_odometer = cols[0].selectbox("Digital Odometer", ['Yes', 'No'])
tachometer = cols[1].selectbox("Tachometer", ['Yes', 'No'])
ventilated_seats = cols[2].selectbox("Ventilated Seats", ['Yes', 'No'])
tinted_glass = cols[3].selectbox("Tinted Glass", ['Yes', 'No'])

fog_lights_rear = cols[0].selectbox("Fog Lights Rear", ['Yes', 'No'])
ledfog_lamps = cols[1].selectbox("LED Fog Lamps", ['Yes', 'No'])
smoke_headlamps = cols[2].selectbox("Smoke Headlamps", ['Yes', 'No'])
chrome_grille = cols[3].selectbox("Chrome Grille", ['Yes', 'No'])

rear_window_wiper = cols[0].selectbox("Rear Window Wiper", ['Yes', 'No'])
ledtaillights = cols[1].selectbox("LED Taillights", ['Yes', 'No'])
outside_rear_view_mirror_turn_indicators = cols[2].selectbox("Outside Rear View Mirror Turn Indicators", ['Yes', 'No'])
adjustable_head_lights = cols[3].selectbox("Adjustable Head Lights", ['Yes', 'No'])

rain_sensing_wiper = cols[0].selectbox("Rain Sensing Wiper", ['Yes', 'No'])
automatic_driving_lights = cols[1].selectbox("Automatic Driving Lights", ['Yes', 'No'])
roof_rail = cols[2].selectbox("Roof Rail", ['Yes', 'No'])
power_antenna = cols[3].selectbox("Power Antenna", ['Yes', 'No'])

integrated_antenna = cols[0].selectbox("Integrated Antenna", ['Yes', 'No'])
removable_convertible_top = cols[1].selectbox("Removable Convertible Top", ['Yes', 'No'])
sun_roof = cols[2].selectbox("Sun Roof", ['Yes', 'No'])
manually_adjustable_exterior_rear_view_mirror = cols[3].selectbox("Manually Adjustable Exterior Rear View Mirror", ['Yes', 'No'])

side_stepper = cols[0].selectbox("Side Stepper", ['Yes', 'No'])
projector_headlamps = cols[1].selectbox("Projector Headlamps", ['Yes', 'No'])
electric_folding_rear_view_mirror = cols[2].selectbox("Electric Folding Rear View Mirror", ['Yes', 'No'])
cornering_foglamps = cols[3].selectbox("Cornering Foglamps", ['Yes', 'No'])

chrome_garnish = cols[0].selectbox("Chrome Garnish", ['Yes', 'No'])
moon_roof = cols[1].selectbox("Moon Roof", ['Yes', 'No'])
alloy_wheels = cols[2].selectbox("Alloy Wheels", ['Yes', 'No'])
rear_window_washer = cols[3].selectbox("Rear Window Washer", ['Yes', 'No'])

leddrls = cols[0].selectbox("LED DRLs", ['Yes', 'No'])
wheel_covers = cols[1].selectbox("Wheel Covers", ['Yes', 'No'])
heated_wing_mirror = cols[2].selectbox("Heated Wing Mirror", ['Yes', 'No'])
power_adjustable_exterior_rear_view_mirror = cols[3].selectbox("Power Adjustable Exterior Rear View Mirror", ['Yes', 'No'])

halogen_headlamps = cols[0].selectbox("Halogen Headlamps", ['Yes', 'No'])
rear_spoiler = cols[1].selectbox("Rear Spoiler", ['Yes', 'No'])
fog_lights_front = cols[2].selectbox("Fog Lights Front", ['Yes', 'No'])
rear_window_defogger = cols[3].selectbox("Rear Window Defogger", ['Yes', 'No'])

cornering_headlamps = cols[0].selectbox("Cornering Headlamps", ['Yes', 'No'])
dual_tone_body_colour = cols[1].selectbox("Dual Tone Body Colour", ['Yes', 'No'])
headlamp_washers = cols[2].selectbox("Headlamp Washers", ['Yes', 'No'])
roof_carrier = cols[3].selectbox("Roof Carrier", ['Yes', 'No'])

ledheadlights = cols[0].selectbox("LED Headlights", ['Yes', 'No'])


tyre_type = cols[0].selectbox("Tyre Type",['radial_runflat','runflat_tubeless',
                                           'tubeless_radial','runflat','radial','tubeless'])

# Section 7: Audio & Connectivity
st.header("Audio & Connectivity")

cols = st.columns(4)
audio_system_remote_control = cols[0].selectbox("Audio System Remote Control", ['Yes', 'No'])
cd_changer = cols[1].selectbox("CD Changer", ['Yes', 'No'])
wireless_phone_charging = cols[2].selectbox("Wireless Phone Charging", ['Yes', 'No'])
speakers_front = cols[3].selectbox("Speakers Front", ["Yes","No"])

internal_storage = cols[0].selectbox("Internal Storage (GB)", ["Yes","No"])
touch_screen_size = cols[1].selectbox("Touch Screen Size (inches)", ['Yes','No'])
wifi_connectivity = cols[2].selectbox("Wi-Fi Connectivity", ['Yes', 'No'])
dvd_player = cols[3].selectbox("DVD Player", ['Yes', 'No'])

speakers_rear = cols[0].selectbox("Speakers Rear", ["Yes",'No'])
radio = cols[1].selectbox("Radio", ['Yes', 'No'])
android_auto = cols[2].selectbox("Android Auto", ['Yes', 'No'])
apple_car_play = cols[3].selectbox("Apple CarPlay", ['Yes', 'No'])

cassette_player = cols[0].selectbox("Cassette Player", ['Yes', 'No'])
touch_screen = cols[1].selectbox("Touch Screen", ['Yes', 'No'])
usb_auxiliary_input = cols[2].selectbox("USB & Auxiliary Input", ['Yes', 'No'])
bluetooth = cols[3].selectbox("Bluetooth", ['Yes', 'No'])

mirror_link = cols[0].selectbox("Mirror Link", ['Yes', 'No'])
rear_entertainment_system = cols[1].selectbox("Rear Entertainment System", ['Yes', 'No'])
integrated2din_audio = cols[2].selectbox("Integrated 2DIN Audio", ['Yes', 'No'])
compass = cols[3].selectbox("Compass", ['Yes', 'No'])

cd_player = cols[0].selectbox("CD Player", ['Yes', 'No'])

# Section 8: Final Details and Prediction
st.header("Final Details")

st.subheader("Estimated Price")
if st.button("Predict"):
    st.write("Your car's estimated price will be displayed here.")
    usr_data = [transmission,ownerno,original_equipment_manufacturer,model,drive_modes,voice_control,smart_key_band,battery_saver,rear_reading_lamp,power_boot,power_steering,real_time_vehicle_tracking,luggage_hook_and_net,cruise_control,seat_lumbar_support,power_windows_front,
     vanity_mirror,gear_shift_indicator,trunk_light,adjustable_headrest,engine_start_stop_button,find_my_car_location,multifunction_steering_wheel,remote_engine_start_stop,active_noise_cancellation,remote_fuel_lid_opener,hands_free_tailgate,remote_trunk_opener,
     lane_change_indicator,glove_box_cooling,tailgate_ajar,steering_wheel_gearshift_paddles,rear_seat_centre_arm_rest,navigation_system,cup_holders_rear,smart_access_card_entry,power_windows_rear,cup_holders_front,rear_acvents,air_quality_control,low_fuel_warning_light,remote_climate_control,
     power_folding3rd_row_seat,steering_mounted_tripmeter,accessory_power_outlet,rear_seat_headrest,remote_horn_light_control,height_adjustable_front_seat_belts,leather_steering_wheel,fabric_upholstery,glove_compartment,adjustable_steering,height_adjustable_driver_seat,air_conditioner,cigarette_lighter,
     dual_tone_dashboard,heater,digital_clock,outside_temperature_display,leather_seats,electronic_multi_tripmeter,rear_folding_table,driving_experience_control_eco,leather_wrap_gear_shift_selector,digital_odometer,tachometer,ventilated_seats,tinted_glass,fog_lights_rear,ledfog_lamps,smoke_headlamps,chrome_grille,
     rear_window_wiper,ledtaillights,outside_rear_view_mirror_turn_indicators,adjustable_head_lights,rain_sensing_wiper,automatic_driving_lights,roof_rail,power_antenna,integrated_antenna,removable_convertible_top,sun_roof,manually_adjustable_exterior_rear_view_mirror,side_stepper,projector_headlamps,electric_folding_rear_view_mirror,
     cornering_foglamps,chrome_garnish,moon_roof,alloy_wheels,rear_window_washer,leddrls,wheel_covers,heated_wing_mirror,power_adjustable_exterior_rear_view_mirror,halogen_headlamps,rear_spoiler,fog_lights_front,rear_window_defogger,cornering_headlamps,dual_tone_body_colour,headlamp_washers,roof_carrier,ledheadlights,traction_control,side_impact_beams,
     seat_belt_warning,rear_seat_belts,power_door_locks,xenon_headlamps,pretensioners_and_force_limiter_seatbelts,side_air_bag_front,anti_lock_braking_system,centeral_locking,hill_descent_control,anti_theft_device,vehicle_stability_control_system,blind_spot_monitor,automatic_head_lamps,knee_airbags,driver_air_bag,engine_immobilizer,crash_sensor,lane_watch_camera,
     front_impact_beams,view360camera,speed_sensing_auto_door_lock,anti_pinch_power_windows,speed_alert,hill_assist,passenger_side_rear_view_mirror,adjustable_seats,rear_camera,geo_fence_alert,clutch_lock,side_air_bag_rear,eletronic_stability_control,child_safety_locks,ebd,centrally_mounted_fuel_tank,brake_assist,passenger_air_bag,sos_emergency_assistance,
     day_night_rear_view_mirror,door_ajar_warning,halogen_headlamps_1,engine_check_warning,isofix_child_seat_mounts,tyre_pressure_monitor,heads_up_display,follow_me_home_headlamps,anti_theft_alarm,impact_sensing_auto_door_lock,keyless_entry,audio_system_remote_control,cd_changer,wireless_phone_charging,speakers_front,internal_storage,touch_screen_size,
     wifi_connectivity,dvd_player,speakers_rear,radio,android_auto,apple_car_play,cassette_player,touch_screen,usb_auxiliary_input,bluetooth,mirror_link,rear_entertainment_system,integrated2din_audio,compass,cd_player,color,turbo_charger,front_brake_type,rear_brake_type,kerb_weight,height,wheel_base,length,width,kilo_meter,model_year,engine_displacement,
     fuel_type,body_type,location,no_of_cylinder,tyre_type]
    
    
    column_names = ['fuel_type', 'body_type', 'kilo_meter', 'transmission', 'ownerno', 'original_equipment_manufacturer', 'model', 'model_year', 'location', 'engine_displacement', 'drive_modes', 'voice_control', 'smart_key_band', 'battery_saver', 'rear_reading_lamp', 'power_boot', 'power_steering', 'real_time_vehicle_tracking', 'luggage_hook_and_net', 'cruise_control', 'seat_lumbar_support', 
                    'power_windows_front', 'vanity_mirror', 'gear_shift_indicator', 'trunk_light', 'adjustable_headrest', 'engine_start_stop_button', 'find_my_car_location', 'multifunction_steering_wheel', 'remote_engine_start_stop', 'active_noise_cancellation', 'remote_fuel_lid_opener', 'hands_free_tailgate', 'remote_trunk_opener', 'lane_change_indicator', 'glove_box_cooling', 'tailgate_ajar', 'steering_wheel_gearshift_paddles', 'rear_seat_centre_arm_rest', 'navigation_system', 'cup_holders_rear', 
                    'smart_access_card_entry', 'power_windows_rear', 'cup_holders_front', 'rear_acvents', 'air_quality_control', 'low_fuel_warning_light', 'remote_climate_control', 'power_folding3rd_row_seat', 'steering_mounted_tripmeter', 'accessory_power_outlet', 'rear_seat_headrest', 'remote_horn_light_control', 'height_adjustable_front_seat_belts', 'leather_steering_wheel', 'fabric_upholstery', 'glove_compartment', 'adjustable_steering', 'height_adjustable_driver_seat', 'air_conditioner', 'cigarette_lighter', 
                    'dual_tone_dashboard', 'heater', 'digital_clock', 'outside_temperature_display', 'leather_seats', 'electronic_multi_tripmeter', 'rear_folding_table', 'driving_experience_control_eco', 'leather_wrap_gear_shift_selector', 'digital_odometer', 'tachometer', 'ventilated_seats', 'tinted_glass', 'fog_lights_rear', 'ledfog_lamps', 'smoke_headlamps', 'chrome_grille', 'rear_window_wiper', 'ledtaillights', 'outside_rear_view_mirror_turn_indicators', 'adjustable_head_lights', 'rain_sensing_wiper', 'automatic_driving_lights', 'roof_rail', 'power_antenna', 'integrated_antenna', 
                    'removable_convertible_top', 'sun_roof', 'manually_adjustable_exterior_rear_view_mirror', 'side_stepper', 'projector_headlamps', 'electric_folding_rear_view_mirror', 'cornering_foglamps', 'chrome_garnish', 'moon_roof', 'alloy_wheels', 'rear_window_washer', 'leddrls', 'wheel_covers', 'heated_wing_mirror', 'power_adjustable_exterior_rear_view_mirror', 'halogen_headlamps', 'rear_spoiler', 'fog_lights_front', 'rear_window_defogger', 'cornering_headlamps', 'dual_tone_body_colour', 'headlamp_washers', 'roof_carrier', 'ledheadlights', 'traction_control', 
                    'side_impact_beams', 'seat_belt_warning', 'rear_seat_belts', 'power_door_locks', 'xenon_headlamps', 'pretensioners_and_force_limiter_seatbelts', 'side_air_bag_front', 'anti_lock_braking_system', 'centeral_locking', 'hill_descent_control', 'anti_theft_device', 'vehicle_stability_control_system', 'blind_spot_monitor', 'automatic_head_lamps', 'knee_airbags', 'driver_air_bag', 'engine_immobilizer', 'crash_sensor', 'lane_watch_camera', 'front_impact_beams', 'view360camera', 'speed_sensing_auto_door_lock', 'anti_pinch_power_windows', 'speed_alert', 'hill_assist', 
                    'passenger_side_rear_view_mirror', 'adjustable_seats', 'rear_camera', 'geo_fence_alert', 'clutch_lock', 'side_air_bag_rear', 'eletronic_stability_control', 'child_safety_locks', 'ebd', 'centrally_mounted_fuel_tank', 'brake_assist', 'passenger_air_bag', 'sos_emergency_assistance', 'day_night_rear_view_mirror', 'door_ajar_warning', 'halogen_headlamps_1', 'engine_check_warning', 'isofix_child_seat_mounts', 'tyre_pressure_monitor', 'heads_up_display', 'follow_me_home_headlamps', 'anti_theft_alarm', 'impact_sensing_auto_door_lock', 'keyless_entry', 
                    'audio_system_remote_control', 'cd_changer', 'wireless_phone_charging', 'speakers_front', 'internal_storage', 'touch_screen_size', 'wifi_connectivity', 'dvd_player', 'speakers_rear', 'radio', 'android_auto', 'apple_car_play', 'cassette_player', 'touch_screen', 'usb_auxiliary_input', 'bluetooth', 'mirror_link', 'rear_entertainment_system', 'integrated2din_audio', 'compass', 'cd_player', 'color', 'turbo_charger', 'no_of_cylinder', 'width', 'length', 'wheel_base', 'height', 'kerb_weight', 'tyre_type', 'front_brake_type', 'rear_brake_type']
    


    data = {var: locals()[var] for var in column_names}
    df = pd.DataFrame([data])


    with open("load_preprocess_data/preprocess_pipeline.pkl", 'rb') as pipeline:
       loaded_pipeline = dill.load(pipeline)
       data = loaded_pipeline.transform(df)
       with open('weights/random_forest.pkl','rb') as model:
           model = dill.load(model)
           predicition = model.predict(data)
           predicition = loaded_pipeline.__getitem__(0)[2].y_ss.inverse_transform([predicition])
           # Display the predicted price to the user
           st.success(f"The estimated price for your car is:   Rs.{round(predicition[0][0],2)}")
           

    


