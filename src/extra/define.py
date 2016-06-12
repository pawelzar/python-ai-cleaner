train_set = open("../train_set", "w")
train_set.write("distance    type    soap    battery    container    clean" + "\n")

for distance in ["close", "medium", "far"]:
    for instance in ["dust", "cat", "water"]:
        for soap in ["low", "medium", "high"]:
            for battery in ["low", "medium", "high"]:
                for container in ["empty", "half", "full"]:
                    line = (distance.ljust(12, " ") +
                            instance.ljust(8, " ") +
                            soap.ljust(8, " ") +
                            battery.ljust(11, " ") +
                            container.ljust(13, " "))
                    train_set.write(line + "True" + "\n")

train_set.close()
