# Сделал интересующие импорты и функцию чтения csv файла с исходными данными
import csv
from statistics import mean


def read_csv(csv_path: str):
  with open(csv_path, 'r', newline='') as r_csv:
    data = list(csv.reader(r_csv, delimiter=',', quotechar='"'))
    #[print(row) for row in data[0:5]]

    return data

data1 = read_csv('Simulative_mod6_basic_python_practice_cases/campaign_data.csv')

#task1
def calc_conv(data: list, column1: int):
    # Extract platform and conversion rate from data
    req_data = [(row[column1], float(row[9])) for row in data[1:]]

    # Create a dictionary to accumulate conversion rates for each platform
    platf_conver = {platf: [] for platf, _ in req_data}

    # Accumulate conversion rates for each platform
    for platf, conv in req_data:
        platf_conver[platf].append(conv)

    # Compute the average conversion rate for each platform
    platf_avg_conv = {platf: round(mean(conv), 3) for platf, conv in platf_conver.items()}

    # Find the platform with the highest average conversion rate#
    #max_conv_plat = max(conv_avg_d.items(), key=lambda x: x[1])[0] #v1
    #max_conv_plat = reduce(lambda x,y: x if x[1] > y[1] else y, conv_avg_d.items()) #v2
    platf_conv_best = max(platf_avg_conv, key=platf_avg_conv.get) #v3

    print(platf_conv_best)
    return platf_conv_best

#task2
most_effective_platform = calc_conv(data1, 4)
#task3
most_successful_campaign_type = calc_conv(data1, 3)
#task4
most_successful_city = calc_conv(data1, 6)


#task5
def calc_mark_cost(data: list):
  req_data = [[row[4], float(row[5]), row[6]] for row in data[1:]]

  platf_data = {}

  for platf, value, city in req_data:
    if platf not in platf_data:
      platf_data[platf] = {}
    if city not in platf_data[platf]:
      platf_data[platf][city] = 0
    platf_data[platf][city] += value

  with open('Simulative_mod6_basic_python_practice_cases/platform_city_results.txt', 'w') as wf:
    for platf, city in platf_data.items():
      sorted_cities = sorted(city.items(), key=lambda x: x[1], reverse=True)
      print(f'Для группы {platf}:', file=wf)

      for name_city, cost in sorted_cities:
        cost_share = round(cost / sum(city.values()) * 100, 2)
        print(f'- Город: {name_city}, доля затрат на рекламу: {cost_share}%', file=wf)


calc_mark_cost(data1)