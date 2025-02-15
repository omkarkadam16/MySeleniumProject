import datetime

def good_morning():
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"Good morning Neha! Have a great day ahead.\nCurrent Time: {current_time}")

good_morning()
