import random
f = open("sampleData_10000.txt")

data = f.read().split("\n")

f.close()


dataset_list = [500,1000,2000]
k_value_set = [1,5,10]

for dataset_size in dataset_list:
    for k in k_value_set:
        current_dataset = []
        search_point_list = []
        file_name = "test_S_" + str(dataset_size) + "_k_" + str(k) + ".in"

        while True:

            if (len(current_dataset) == dataset_size):
                break
            
            random_index = random.randint(0, len(data)-2)
            data_row = data[random_index]
            if (data_row not in current_dataset):
                current_dataset.append(data_row)
                lat_val = float(data_row.split(" ")[2]) - random.randint(1,4)/4
                lat_val = round(lat_val,2)
                lon_val = float(data_row.split(" ")[3]) - random.randint(1,4)/4
                lon_val = round(lon_val,2)
                search_point = "S " + data_row.split(" ")[1] + " " + str(lat_val) + " " + str(lon_val) + " " + str(k)
                search_point_list.append(search_point)


        final_str = "\n".join(item for item in search_point_list)

        f = open(file_name, 'w')
        f.write(final_str)
        f.close()
