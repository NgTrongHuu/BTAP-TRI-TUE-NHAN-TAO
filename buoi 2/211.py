import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

distance = ctrl.Antecedent(np.arange(0, 51, 1), 'distance')
traffic = ctrl.Antecedent(np.arange(0, 101, 1), 'traffic')
demand = ctrl.Antecedent(np.arange(0, 101, 1), 'demand')
weather = ctrl.Antecedent(np.arange(0, 11, 1), 'weather')
rating = ctrl.Antecedent(np.arange(0, 6, 1), 'rating')
punctuality = ctrl.Antecedent(np.arange(0, 101, 1), 'punctuality')

price = ctrl.Consequent(np.arange(0, 101, 1), 'price')
bonus = ctrl.Consequent(np.arange(0, 101, 1), 'bonus')

distance['ngan'] = fuzzy.trapmf(distance.universe, [0, 0, 3, 8])
distance['trung_binh'] = fuzzy.trimf(distance.universe, [5, 12, 20])
distance['xa'] = fuzzy.trimf(distance.universe, [15, 30, 45])
distance['rat_xa'] = fuzzy.trapmf(distance.universe, [35, 50, 51, 51]) 

traffic['thap'] = fuzzy.trapmf(traffic.universe, [0, 0, 30, 50])
traffic['trung_binh'] = fuzzy.trimf(traffic.universe, [30, 50, 70])
traffic['cao'] = fuzzy.trapmf(traffic.universe, [60, 90, 101, 101])

demand['thap'] = fuzzy.trapmf(demand.universe, [0, 0, 40, 60])
demand['trung_binh'] = fuzzy.trimf(demand.universe, [40, 60, 80])
demand['cao'] = fuzzy.trapmf(demand.universe, [70, 90, 101, 101])

weather['tot'] = fuzzy.trimf(weather.universe, [0, 0, 5])
weather['trung_binh'] = fuzzy.trimf(weather.universe, [3, 5, 8])
weather['xau'] = fuzzy.trapmf(weather.universe, [7, 10, 11, 11])

rating['kem'] = fuzzy.trapmf(rating.universe, [0, 0, 1, 3])
rating['trung_binh'] = fuzzy.trimf(rating.universe, [2, 3, 4])
rating['tot'] = fuzzy.trapmf(rating.universe, [3.5, 5, 6, 6])

punctuality['tre'] = fuzzy.trapmf(punctuality.universe, [0, 0, 30, 60])
punctuality['dung_gio'] = fuzzy.trimf(punctuality.universe, [50, 75, 90])
punctuality['som'] = fuzzy.trapmf(punctuality.universe, [80, 100, 101, 101])


price['thap'] = fuzzy.trimf(price.universe, [0, 0, 30])
price['trung_binh'] = fuzzy.trimf(price.universe, [25, 50, 75])
price['cao'] = fuzzy.trimf(price.universe, [60, 80, 90])
price['rat_cao'] = fuzzy.trimf(price.universe, [80, 100, 100])

bonus['khong'] = fuzzy.trimf(bonus.universe, [0, 0, 10])
bonus['it'] = fuzzy.trimf(bonus.universe, [5, 20, 40])
bonus['trung_binh'] = fuzzy.trimf(bonus.universe, [30, 50, 70])
bonus['cao'] = fuzzy.trimf(bonus.universe, [60, 100, 100])

rules = [
    ctrl.Rule(distance['ngan'] & traffic['thap'] & demand['thap'], price['thap']),
    ctrl.Rule(distance['ngan'] & traffic['trung_binh'] & demand['cao'], price['trung_binh']),
    ctrl.Rule(distance['trung_binh'] & traffic['cao'] & demand['cao'], price['cao']),
    ctrl.Rule(distance['xa'] & traffic['trung_binh'] & weather['tot'], price['trung_binh']),
    ctrl.Rule(distance['xa'] & traffic['cao'] & weather['xau'], price['rat_cao']),
    ctrl.Rule(distance['rat_xa'] & traffic['cao'] & demand['cao'], price['rat_cao']),
    ctrl.Rule(distance['trung_binh'] & traffic['thap'] & demand['thap'], price['trung_binh']),
    ctrl.Rule(distance['ngan'] & traffic['cao'] & weather['xau'], price['trung_binh']),
    ctrl.Rule(distance['rat_xa'] & weather['xau'], price['rat_cao']),
    ctrl.Rule(distance['trung_binh'] & traffic['trung_binh'] & weather['trung_binh'], price['trung_binh']),
    ctrl.Rule(rating['tot'] & punctuality['som'], bonus['cao']),
    ctrl.Rule(rating['trung_binh'] & punctuality['dung_gio'], bonus['trung_binh']),
    ctrl.Rule(rating['kem'] & punctuality['tre'], bonus['khong']),
    ctrl.Rule(distance['xa'] & traffic['cao'] & punctuality['dung_gio'], bonus['cao']),
    ctrl.Rule(distance['trung_binh'] & traffic['trung_binh'] & rating['tot'], bonus['trung_binh']),
    ctrl.Rule(rating['kem'] & punctuality['tre'], bonus['khong']),
    ctrl.Rule(distance['rat_xa'] & weather['xau'] & rating['tot'], bonus['cao']),
    ctrl.Rule(distance['ngan'] & rating['trung_binh'] & punctuality['dung_gio'], bonus['it']),
    ctrl.Rule(distance['xa'] & traffic['cao'] & punctuality['tre'], bonus['it']),
    ctrl.Rule(distance['trung_binh'] & weather['trung_binh'] & rating['tot'], bonus['trung_binh'])
]

grab_ctrl = ctrl.ControlSystem(rules)
simulation = ctrl.ControlSystemSimulation(grab_ctrl)

print("----- NHẬP DỮ LIỆU GRAB-BIKE -----")
try:
    simulation.input['distance'] = float(input("Nhập khoảng cách (0-50 km): "))
    simulation.input['traffic'] = float(input("Nhập tình trạng giao thông (0-100%): "))
    simulation.input['demand'] = float(input("Nhập mức cầu (0-100%): "))
    simulation.input['weather'] = float(input("Nhập điều kiện thời tiết (0:Tốt - 10:Xấu): "))
    simulation.input['rating'] = float(input("Nhập đánh giá tài xế (1-5 sao): "))
    simulation.input['punctuality'] = float(input("Nhập độ đúng giờ (0-100%): "))

    simulation.compute()
    print("\n----- KẾT QUẢ -----")
    print(f"Giá cước tính toán: {simulation.output['price']:.2f}")
    print(f"Điểm thưởng tài xế: {simulation.output['bonus']:.2f}")
except Exception as e:
    print(f"Lỗi hệ thống: {e}")