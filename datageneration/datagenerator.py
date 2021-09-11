import random
import time
from datetime import datetime

lat_initial_val = float(input("Latitude Start Value : "))
lon_initial_val = float(input("Longitude Start Value : "))

dataset_list = [1000, 2000, 5000, 10000]
category_list = ["restaurant", "education", "hospital"]

random.seed(datetime.now())



for dataset_size in dataset_list:

    item_id = 1
    current_dataset = []
    file_name = "sampleData_" + str(dataset_size) + ".txt"

    while True:

        if (len(current_dataset) == dataset_size):
            break

        cur_milli_seconds = round(time.time()) - random.randint(1000000000,10000000000)
        category = category_list[random.randint(0,2)]

        random_num = random.randint(1,5)

        if ((item_id%random_num) != 0):
            if (random_num%2 == 0):
                latitude = lat_initial_val + item_id%random_num + (item_id%random_num) * (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
            else:
                latitude = lat_initial_val - item_id%random_num + (item_id%random_num) * (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
        else:
            if (random_num%2 == 0):
                latitude = lat_initial_val + item_id%random_num + (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
            else:
                latitude = lat_initial_val - item_id%random_num + (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100

        latitude = round(latitude,9)     
       
        
        random_num = random.randint(1,5)
        
        cur_milli_seconds = round(time.time()) - random.randint(1,1000000)

        if ((item_id%random_num) != 0):
            if (random_num%2 == 0):
                longitude = lon_initial_val + item_id%random_num + (item_id%random_num) * (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
            else:
                longitude = lon_initial_val - item_id%random_num + (item_id%random_num) * (cur_milli_seconds/((len(str(cur_milli_seconds))**10)*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
        else:
            if (random_num%2 == 0):
                longitude = lon_initial_val + item_id%random_num + cur_milli_seconds/((len(str(cur_milli_seconds))**10*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100
            else:
                longitude = lon_initial_val - item_id%random_num + cur_milli_seconds/((len(str(cur_milli_seconds))**10*random_num)) - random.randint(1,100)/100 + random.randint(1,100)/100

        longitude = round(longitude,10)   
       
        
        data_row = str(item_id) + " " + category + " " + str(latitude) + " " + str(longitude)
        
        if (data_row not in current_dataset):
            current_dataset.append(data_row)
            item_id += 1


    resturant_list = []
    education_list = []
    hospital_list = []
    final_list = []

    index = 1
    for i in current_dataset:
        space_after_id = i[i.index(" ")::]
        i = "id" + str(index) + space_after_id
        if ("restaurant" in i):
            resturant_list.append(i)
            index += 1

    for i in current_dataset:
        space_after_id = i[i.index(" ")::]
        i = "id" + str(index) + space_after_id
        if ("hospital" in i):
            hospital_list.append(i)
            index += 1

    for i in current_dataset:
        space_after_id = i[i.index(" ")::]
        i = "id" + str(index) + space_after_id
        if ("education" in i):
            education_list.append(i)
            index += 1
        

    final_list.extend(resturant_list)
    final_list.extend(hospital_list)
    final_list.extend(education_list)

    print ("Final List Size : ", len(final_list))
    final_str = "\n".join(item for item in final_list)

    f = open(file_name, 'w')
    f.write(final_str)
    f.close()
