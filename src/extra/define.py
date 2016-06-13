'''train_set = open("../train", "w")
train_set.write("DISTANCE    TYPE    SOAP    BATTERY    CONTAINER    CLEAN" + "\n")

for distance in ["close", "medium", "far"]:
    for instance in ["dust", "cat", "water"]:
        for soap in ["low", "medium", "high"]:
            for battery in ["low", "medium", "high"]:
                for container in ["empty", "half", "full"]:
                    # result = {"low": "False"}.get(battery, "True")
                    result = "False" if battery == "low" else \
                        ("False" if (instance == "cat" or instance == "water") and soap == "low"
                         else "False" if container == "full" else "True")
                    line = (distance.ljust(12, " ") +
                            instance.ljust(8, " ") +
                            soap.ljust(8, " ") +
                            battery.ljust(11, " ") +
                            container.ljust(13, " "))
                    train_set.write(line + result + "\n")

train_set.close()'''


train_set = open("../train_refill", "w")
train_set.write("DIST_STA    DIST_BIN    BATTERY    SOAP    CONTAINER    DECISION" + "\n")

for dist_station in ["close", "medium", "far"]:
    for dist_bin in ["close", "medium", "far"]:
        for battery in ["low", "medium", "high"]:
            for soap in ["low", "medium", "high"]:
                for container in ["empty", "half", "full"]:
                    # result = {"low": "False"}.get(battery, "True")
                    '''result = "bin" if ((dist_bin == "close" or dist_bin == "medium") and
                                       (dist_station == "medium" or dist_station == "far") and
                                       container == "full") \
                        else "station"'''
                    result = "bin" if container == "full" else "station"
                    line = (dist_station.ljust(12, " ") +
                            dist_bin.ljust(12, " ") +
                            battery.ljust(11, " ") +
                            soap.ljust(8, " ") +
                            container.ljust(13, " "))
                    train_set.write(line + result + "\n")

train_set.close()
