# -*- coding: 1251 -*-

# Сделал интересующие импорты и функцию чтения csv файла с исходными данными

import csv
from statistics import mean


def read_csv(csv_path: str):
    with open(csv_path, "r", newline="") as r_csv:
        data = list(csv.reader(r_csv, delimiter=",", quotechar='"'))
        # [print(row) for row in data[0:5]]

        return data


data1 = read_csv("Simulative_mod6_basic_python_practice_cases/campaign_data.csv")


# task1
def calc_conv(data: list, column1: int):
    # Extract platform and conversion rate from data
    req_data = [(row[column1], float(row[9])) for row in data[1:]]

    # Create a dictionary to accumulate conversion rates for each platform
    platf_conver = {platf: [] for platf, _ in req_data}

    # Accumulate conversion rates for each platform
    for platf, conv in req_data:
        platf_conver[platf].append(conv)

    # Compute the average conversion rate for each platform
    platf_avg_conv = {
        platf: round(mean(conv), 3) for platf, conv in platf_conver.items()
    }

    # Find the platform with the highest average conversion rate#
    # max_conv_plat = max(conv_avg_d.items(), key=lambda x: x[1])[0] #v1
    # max_conv_plat = reduce(lambda x,y: x if x[1] > y[1] else y, conv_avg_d.items()) #v2
    platf_conv_best = max(platf_avg_conv, key=platf_avg_conv.get)  # v3

    print(platf_conv_best)
    return platf_conv_best


# task2
most_effective_platform = calc_conv(data1, 4)
# task3
most_successful_campaign_type = calc_conv(data1, 3)
# task4
most_successful_city = calc_conv(data1, 6)


# task5
def calc_mark_cost(data: list):
    req_data = [[row[4], float(row[5]), row[6]] for row in data[1:]]

    platf_data = {}

    for platf, value, city in req_data:
        if platf not in platf_data:
            platf_data[platf] = {}
        if city not in platf_data[platf]:
            platf_data[platf][city] = 0
        platf_data[platf][city] += value

    with open(
        "Simulative_mod6_basic_python_practice_cases/platform_city_results.txt", "w"
    ) as wf:
        for platf, city in platf_data.items():
            sorted_cities = sorted(city.items(), key=lambda x: x[1], reverse=True)
            print(f"Для группы {platf}:", file=wf)

            for name_city, cost in sorted_cities:
                cost_share = round(cost / sum(city.values()) * 100, 2)
                print(
                    f"- Город: {name_city}, доля затрат на рекламу: {cost_share}%",
                    file=wf,
                )


calc_mark_cost(data1)


# task6
def calculate_average_budget(csv_file_path: str, platform: str):
    with open(csv_file_path, "r", newline="") as open_csv_read:
        data = list(csv.reader(open_csv_read, delimiter=",", quotechar='"'))
        # [print(row) for row in data[1:5]]

        req_data = [(row[4], float(row[5])) for row in data[1:]]
        # print(req_data)

        platf_cost = {platf: [] for platf, cost in req_data}
        # print(platf_cost)

        for platf, cost in req_data:
            platf_cost[platf].append(cost)

        platf_avg_cost = {
            platf: round(mean(cost), 2) for platf, cost in platf_cost.items()
        }
        # print(platf_avg_cost)

        res = platf_avg_cost.get(platform)

        print(res)
        return res


calculate_average_budget(
    "Simulative_mod6_basic_python_practice_cases/campaign_data.csv", "Telegram"
)


# task7
from datetime import datetime, timedelta


def get_missing_campaign_dates(csv_path: str):

    with open(csv_path, "r") as op_csv:
        data = list(csv.reader(op_csv))
        # [print(row) for row in data[:10]]

        req_data = [row[1] for row in data[1:]]
        # print(req_data)

        dates_camp = []
        [
            dates_camp.append(datetime.strptime(date, "%Y-%m-%d"))
            for date in req_data
            if date not in dates_camp
        ]
        # print(dates_camp)

        start_date = dates_camp[0]
        end_date = dates_camp[-1]
        all_dates = [
            start_date + timedelta(days=i)
            for i in range((end_date - start_date).days + 1)
        ]
        # print(all_dates)

        yield from (date for date in all_dates if date not in dates_camp)


generator = get_missing_campaign_dates(
    "Simulative_mod6_basic_python_practice_cases/campaign_data.csv"
)
print(next(generator))
print(next(generator))
print(next(generator))


# task8
def group_campaign_data(csv_path: str):
    with open(csv_path, "r") as op_csv:
        data = list(csv.reader(op_csv))
        # [print(row) for row in data[0:5]]

        req_data = [(row[5], row[6], row[8]) for row in data[1:]]
        # print(req_data)

        opt_data = [(city, float(click), int(cost)) for cost, city, click in req_data]
        # print(opt_data)

        city_data = {}
        for city, click, cost in opt_data:
            if city not in city_data:
                city_data[city] = {
                    "Город": city,
                    "Количество кликов": click,
                    "Суммарный бюджет": cost,
                }
            else:
                city_data[city]["Количество кликов"] += click
                city_data[city]["Суммарный бюджет"] += cost

        res = list(city_data.values())
        # print(res)

        sorted_res = sorted(res, key=lambda x: x["Город"])
        # print(sorted_res)

        return sorted_res


group_campaign_data("Simulative_mod6_basic_python_practice_cases/campaign_data.csv")


# task9
def campaign_generator(csv_path: str, seek_city: str, seek_cost: int):
    with open(csv_path, "r", newline="") as op_csv:
        data = list(csv.reader(op_csv, delimiter=",", quotechar='"'))
        # [print(row) for row in data[0:5]]

        req_data = [
            (row[0], row[3], row[4], row[5], row[6], row[-1])
            for row in data[1:]
            if row[6] == seek_city and int(row[5]) > seek_cost
        ]
        # [print(row) for row in req_data]

        res_gen = (
            {
                "ID Кампании": camp_id,
                "Тип": ttype,
                "Платформа": platf,
                "Доход": rev,
            }
            for camp_id, ttype, platf, _, _, rev in req_data
        )

        yield from res_gen


generator = campaign_generator(
    "Simulative_mod6_basic_python_practice_cases/campaign_data.csv",
    "Москва",
    25000,
)
print(next(generator))
print(next(generator))
print(next(generator))
