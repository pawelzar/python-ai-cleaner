train_set = open("../train_set", "w")
train_set.write("DISTANCE    TYPE    SOAP    BATTERY    CONTAINER    CLEAN" + "\n")

for distance in ["close", "medium", "far"]:
    for instance in ["dust", "cat", "water"]:
        for soap in ["low", "medium", "high"]:
            for battery in ["low", "medium", "high"]:
                for container in ["empty", "half", "full"]:
                    # result = {"low": "False"}.get(battery, "True")
                    result = "False" if battery == "low" else \
                        ("False" if (instance == "cat" or instance == "water") and soap == "low" else "True")
                    line = (distance.ljust(12, " ") +
                            instance.ljust(8, " ") +
                            soap.ljust(8, " ") +
                            battery.ljust(11, " ") +
                            container.ljust(13, " "))
                    train_set.write(line + result + "\n")

train_set.close()
