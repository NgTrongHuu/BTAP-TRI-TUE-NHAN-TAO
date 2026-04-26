import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

demand = ctrl.Antecedent(np.arange(0, 11, 1), 'demand')
pressure = ctrl.Antecedent(np.arange(0, 11, 1), 'pressure')
reputation = ctrl.Antecedent(np.arange(0, 6, 1), 'reputation')
margin = ctrl.Antecedent(np.arange(0, 101, 1), 'margin')
seasonal = ctrl.Antecedent(np.arange(0, 11, 1), 'seasonal')
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

demand['thap'] = fuzzy.trimf(demand.universe, [0, 0, 5])
demand['trung_binh'] = fuzzy.trimf(demand.universe, [3, 5, 7])
demand['cao'] = fuzzy.trimf(demand.universe, [6, 10, 10])
pressure['thap'] = fuzzy.trimf(pressure.universe, [0, 0, 5])
pressure['trung_binh'] = fuzzy.trimf(pressure.universe, [3, 5, 7])
pressure['cao'] = fuzzy.trimf(pressure.universe, [6, 10, 10])
reputation['thap'] = fuzzy.trimf(reputation.universe, [0, 0, 4])
reputation['cao'] = fuzzy.trimf(reputation.universe, [4, 5, 5])
margin['thap'] = fuzzy.trimf(margin.universe, [0, 0, 40])
margin['trung_binh'] = fuzzy.trimf(margin.universe, [30, 50, 70])
margin['cao'] = fuzzy.trimf(margin.universe, [60, 100, 100])
seasonal['khong'] = fuzzy.trimf(seasonal.universe, [0, 0, 5])
seasonal['trung_binh'] = fuzzy.trimf(seasonal.universe, [3, 5, 7])
seasonal['cao'] = fuzzy.trimf(seasonal.universe, [6, 10, 10])
discount['rat_thap'] = fuzzy.trimf(discount.universe, [0, 0, 5])
discount['thap'] = fuzzy.trimf(discount.universe, [5, 10, 20])
discount['trung_binh'] = fuzzy.trimf(discount.universe, [15, 25, 40])
discount['cao'] = fuzzy.trimf(discount.universe, [40, 70, 70])

rules = [
    ctrl.Rule(demand['cao'] & pressure['thap'] & margin['thap'], discount['rat_thap']),
    ctrl.Rule(demand['thap'] & pressure['cao'] & margin['cao'], discount['cao']),
    ctrl.Rule(reputation['cao'] & margin['trung_binh'] & seasonal['cao'], discount['trung_binh']),
    ctrl.Rule(pressure['cao'] & seasonal['cao'] & margin['cao'], discount['cao']),
    ctrl.Rule(reputation['thap'] & demand['trung_binh'] & margin['thap'], discount['trung_binh']),
    ctrl.Rule(demand['cao'] & seasonal['khong'] & pressure['thap'], discount['rat_thap']),
    ctrl.Rule(margin['cao'] & pressure['trung_binh'] & seasonal['trung_binh'], discount['trung_binh'])
]

special_sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

print("----- NHẬP DỮ LIỆU HÀNG ĐẶC BIỆT -----")
try:
    special_sim.input['demand'] = float(input("Nhu cầu sản phẩm (0-10): "))
    special_sim.input['pressure'] = float(input("Áp lực cạnh tranh (0-10): "))
    special_sim.input['reputation'] = float(input("Uy tín cửa hàng (1-5 sao): "))
    special_sim.input['margin'] = float(input("Biên lợi nhuận (%): "))
    special_sim.input['seasonal'] = float(input("Nhu cầu theo mùa (0-10): "))

    special_sim.compute()
    print(f"\n=> Giảm giá áp dụng: {special_sim.output['discount']:.2f}%")
except:
    print("Lỗi nhập liệu!")