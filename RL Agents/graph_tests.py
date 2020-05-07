import matplotlib.pyplot as plt

# For one enemy x = 1, diff is different locations while x_2 is same location (Default)

x_1_norm = {5: [3440, 3510, 3295, 2573, 3387, 3078, 3505, 3451, 3185, 3424],
            7: [1515, 1300, 3390, 3464, 3445, 3184, 3182, 3503, 3450, 1515],
            9: [3231, 3374, 3575, 3386, 3387, 3336, 2311, 2617, 2770, 2365],
            11: [1759, 3497, 2668, 3229, 1615, 3028, 2500, 3284, 3122, 3393],
            13: [1562, 3074, 2459, 1562, 3232, 2338, 1562, 1562, 3017, 2549],
            15: [2407, 1771, 1772, 3019, 1409, 1960, 1960, 1772, 1740, 1565],
            17: [2164, 1195, 1038, 1310, 1567, 1564, 1361, 936, 1102, 1611],
            19: [1200, 657, 657, 1200, 1042, 1143, 1358, 1357, 657, 1358],
            21: [492, 492, 492, 492, 492, 492, 492, 492, 492, 492],
            23: [41, 41, 41, 41, 41, 41, 41, 41, 41, 41]}

keys = sorted(x_1_norm)
plt.boxplot([x_1_norm[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_1_norm[k]) / len(x_1_norm[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 1 Enemy")
plt.show()



x_1_diff = {5: [3184, 3184, 3184, 3393, 3184],
            7: [3028, 1414, 1464],
            9: [2673, 1563, 2440, 3132, 2313],
            11: [2139],
            13: [1952, 2553, 1562, 3026, 1563],
            15: [1097, 992, 1148, 1859, 1311, 1861, 992, 1459],
            17: [1146, 1303, 1306, 1042, 1460, 928, 1084, 1042, 1896, 1088],
            19: [589, 589, 383, 800, 383, 800, 383, 853, 383, 589],
            21: [583, 686, 668, 705, 668, 686, 668, 705, 668, 583]}


keys = sorted(x_1_diff)
plt.boxplot([x_1_diff[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_1_diff[k]) / len(x_1_diff[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 1 Enemy")
plt.show()

# For two enemies x = 2, diff is different locations while x_2 is same location (default starting location

x_2_norm = {5: [886, 886, 886, 886, 886, 886, 886, 886, 886, 886],
            7: [267, 267, 267, 267, 267, 267, 267, 267, 267, 267],
            9: [1203, 1740, 1206, 1515, 1203, 1203, 1565, 1565, 1254, 1362],
            11: [153, 153, 153, 153, 153, 153, 153, 153, 153, 153],
            13: [432, 432, 432, 432, 432, 432, 432, 432, 432, 432],
            15: [42, 42, 42, 42, 42, 42, 42, 42, 42, 42],
            17: [345, 345, 345, 345, 345, 345, 345, 345, 345, 345],
            19: [218, 218, 218, 218, 218, 218, 218, 218, 218, 218],
            21: [262, 262, 262, 262, 262, 262, 262, 262, 262, 262],
            23: [279, 279, 279, 279, 279, 279, 279, 279, 279, 279]}

keys = sorted(x_2_norm)
plt.boxplot([x_2_norm[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_2_norm[k]) / len(x_2_norm[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 2 Enemies")
plt.show()


x_2_diff = {5: [897, 846, 1306, 1707, 1404, 602, 1408, 2853, 1250, 1707, 1250, 1365, 1353, 846, 1250, 1211, 1250, 1211, 1562, 899],
            7: [1305, 1001, 1299, 844, 1355, 844, 1355, 1209, 1299, 1261, 1355, 803, 1355, 1209, 1299, 791, 1513, 1416, 1612, 1305],
            9: [272, 272, 1253, 272, 1154, 272, 1405, 272, 1257, 272, 1308, 272, 1405, 272, 1405, 272, 1411, 272, 1154, 272],
            11: [569, 825, 456, 632, 456, 1202, 456, 825, 456, 902, 456, 902, 456, 620, 456, 825, 456, 625, 456, 672],
            13: [1077, 1077, 104, 1077, 104, 1077, 104, 1077, 104, 1077, 104, 1077, 104, 1180, 104, 1077, 104, 1077, 104, 1077],
            15: [282, 282, 356, 282, 356, 282, 356, 282, 356, 282, 354, 282, 796, 282, 356, 282, 356, 282, 354, 282],
            17: [172, 505, 135, 172, 135, 172, 135, 927, 135, 712, 135, 505, 135, 172, 135, 172, 135, 768, 135, 172],
            19: [265, 265, 601, 265, 667, 265, 601, 265, 601, 265, 658, 265, 601, 265, 712, 265, 601, 265, 601, 265],
            21: [233, 233, 76, 233, 76, 233, 76, 233, 76, 233, 76, 233, 76, 233, 76, 233, 76, 233, 76, 233],
            23: [215, 219, 248, 219, 248, 219, 248, 215, 248, 215, 248, 215, 248, 219, 248, 215, 248, 219, 248, 219]}

keys = sorted(x_2_diff)
plt.boxplot([x_2_diff[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_2_diff[k]) / len(x_2_diff[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 2 Enemies")
plt.show()

# For three enemies x = 3

x_3_norm = {5: [783, 783, 783, 783, 783, 783, 468, 468, 468, 468],
            7: [480, 480, 480, 480, 480, 480, 480, 480, 480, 480],
            9: [1206, 1396, 872, 1105, 1201, 1024, 1257, 1105, 1049, 1105],
            11: [1201, 1086, 938, 1142, 793, 1086, 1141, 1201, 883, 1053],
            13: [115, 115, 115, 115, 115, 115, 115, 115, 115, 115],
            15: [184, 184, 184, 184, 184, 184, 184, 184, 184, 184],
            17: [187, 187, 187, 187, 187, 187, 187, 187, 187, 187],
            19: [104, 104, 104, 104, 104, 104, 104, 104, 104, 104],
            21: [80, 80, 80, 80, 80, 80, 80, 80, 80, 80],
            23: [62, 62, 62, 62, 62, 62, 62, 62, 62, 62]}

keys = sorted(x_3_norm)
plt.boxplot([x_3_norm[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_3_norm[k]) / len(x_3_norm[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 3 Enemies")
plt.show()

x_3_diff = {5: [208, 208, 830, 208, 830, 208, 830, 208, 830, 208],
            7: [252, 252, 1461, 252, 778, 252, 1355, 252, 778, 252],
            9: [472, 472, 339, 472, 339, 472, 339, 472, 339, 472],
            11: [407, 407, 158, 407, 490, 407, 158, 407, 158, 407],
            13: [295, 305, 142, 305, 142, 305, 142, 305, 142, 305],
            15: [235, 235, 67, 286, 67, 286, 67, 286, 67, 235],
            17: [54, 54, 194, 54, 194, 54, 194, 54, 194, 54],
            19: [17, 17, 28, 17, 28, 17, 28, 17, 28, 17],
            21: [148, 148, 195, 148, 195, 148, 195, 148, 195, 148],
            23: [125, 125, 191, 125, 191, 125, 191, 125, 191, 125]}


keys = sorted(x_3_diff)
plt.boxplot([x_3_diff[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_3_diff[k]) / len(x_3_diff[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 3 Enemies")
plt.show()

# For four enemies x = 4

x_4_diff = {5: [208, 208, 178, 208, 178, 208, 178, 208, 178, 208],
            7: [468, 468, 176, 468, 176, 468, 176, 468, 176, 468],
            9: [158, 158, 348, 158, 348, 158, 348, 158, 348, 158],
            11: [228, 228, 224, 228, 224, 228, 224, 228, 224, 228],
            13: [74, 74, 74, 74, 74, 74, 74, 74, 74, 74],
            15: [59, 59, 59, 59, 59, 59, 59, 59, 59, 59],
            17: [54, 54, 57, 54, 57, 54, 57, 54, 57, 54],
            19: [17, 17, 17, 17, 17, 17, 17, 17, 17, 17],
            21: [81, 81, 132, 81, 132, 81, 132, 81, 132, 81],
            23: [10, 10, 22, 10, 22, 10, 22, 10, 22, 10]}

keys = sorted(x_4_diff)
plt.boxplot([x_4_diff[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_4_diff[k]) / len(x_4_diff[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 4 Enemies")
plt.show()


x_4_norm = {5: [123, 123, 123, 123, 123, 123, 123, 123, 123, 123],
            7: [287, 383, 287, 383, 287, 287, 383, 287, 287, 383],
            9: [265, 265, 265, 265, 265, 265, 265, 265, 265, 265],
            11: [96, 96, 96, 96, 96, 96, 96, 96, 96, 96],
            13: [63, 63, 63, 63, 63, 63, 63, 63, 63, 63],
            15: [72, 72, 72, 72, 72, 72, 72, 72, 72, 72],
            17: [136, 136, 136, 136, 136, 136, 136, 136, 136, 136],
            19: [79, 79, 79, 79, 79, 79, 79, 79, 79, 79],
            21: [63, 63, 63, 63, 63, 63, 63, 63, 63, 63],
            23: [63, 63, 63, 63, 63, 63, 63, 63, 63, 63]}

keys = sorted(x_4_norm)
plt.boxplot([x_4_norm[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_4_norm[k]) / len(x_4_norm[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 4 Enemies")
plt.show()


#For five enemies x = 5

x_5_diff = {5: [200, 200, 511, 200, 511, 200, 511, 200, 511, 200],
            7: [275, 275, 246, 275, 246, 275, 246, 275, 246, 275],
            9: [98, 98, 619, 98, 619, 98, 619, 98, 253, 98],
            11: [150, 150, 262, 150, 262, 150, 262, 150, 262, 150],
            13: [54, 54, 207, 54, 207, 54, 207, 54, 207, 54],
            15: [80, 80, 54, 80, 54, 80, 54, 80, 54, 80],
            17: [20, 20, 36, 20, 36, 20, 36, 20, 36, 20],
            19: [22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
            21: [39, 39, 73, 39, 73, 39, 73, 39, 73, 39],
            23: [72, 72, 39, 72, 39, 72, 39, 72, 39, 72]}

keys = sorted(x_5_diff)
plt.boxplot([x_5_diff[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_5_diff[k]) / len(x_5_diff[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 5 Enemies")
plt.show()

x_5_norm = {5: [147, 147, 147, 147, 147, 147, 147, 147, 147, 147],
            7: [293, 293, 293, 293, 293, 293, 293, 293, 293, 293],
            9: [258, 258, 258, 258, 258, 258, 258, 258, 258, 258],
            11: [54, 54, 54, 54, 54, 54, 54, 54, 54, 54],
            13: [51, 51, 51, 51, 51, 51, 51, 51, 51, 51],
            15: [105, 105, 105, 105, 105, 105, 105, 105, 105, 105],
            17: [16, 16, 16, 16, 16, 16, 16, 16, 16, 16],
            19: [22, 22, 22, 22, 22, 22, 22, 22, 22, 22],
            21: [21, 21, 21, 21, 21, 21, 21, 21, 21, 21],
            23: [23, 23, 23, 23, 23, 23, 23, 23, 23, 23]}

keys = sorted(x_5_norm)
plt.boxplot([x_5_norm[k] for k in keys], positions=keys)  # box-and-whisker plot
plt.plot(keys, [sum(x_5_norm[k]) / len(x_5_norm[k]) for k in keys], '-o')
plt.xlabel("Distance untill evade bot overtakes exploit bot (closest_dist)")
plt.ylabel("Average score")
plt.title("Evade-Exploit Hybrid Performance for 5 Enemies")
plt.show()


