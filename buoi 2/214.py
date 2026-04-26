import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

density = ctrl.Antecedent(np.arange(0, 11, 1), 'density')
urgency = ctrl.Antecedent(np.arange(0, 11, 1), 'urgency')
load = ctrl.Antecedent(np.arange(0, 11, 1), 'load')
traffic = ctrl.Antecedent(np.arange(0, 11, 1), 'traffic')
profit = ctrl.Antecedent(np.arange(0, 11, 1), 'profit')
combine = ctrl.Consequent(np.arange(0, 11, 1), 'combine')
priority = ctrl.Consequent(np.arange(0, 11, 1), 'priority')

density['thap'] = fuzzy.trimf(density.universe, [0, 0, 4])
density['trung_binh'] = fuzzy.trimf(density.universe, [3, 5, 7])
density['cao'] = fuzzy.trimf(density.universe, [6, 10, 10])
urgency['thap'] = fuzzy.trimf(urgency.universe, [0, 0, 4])
urgency['trung_binh'] = fuzzy.trimf(urgency.universe, [3, 5, 7])
urgency['cao'] = fuzzy.trimf(urgency.universe, [6, 10, 10])
load['thap'] = fuzzy.trimf(load.universe, [0, 0, 4])
load['cao'] = fuzzy.trimf(load.universe, [6, 10, 10])
traffic['thap'] = fuzzy.trimf(traffic.universe, [0, 0, 4])
traffic['trung_binh'] = fuzzy.trimf(traffic.universe, [3, 5, 7])
traffic['cao'] = fuzzy.trimf(traffic.universe, [6, 10, 10])
profit['trung_binh'] = fuzzy.trimf(profit.universe, [3, 5, 7])
profit['cao'] = fuzzy.trimf(profit.universe, [6, 10, 10])
combine['it'] = fuzzy.trimf(combine.universe, [0, 0, 4])
combine['mot_so'] = fuzzy.trimf(combine.universe, [3, 5, 7])
combine['nhieu'] = fuzzy.trimf(combine.universe, [6, 10, 10])
priority['thap'] = fuzzy.trimf(priority.universe, [0, 0, 4])
priority['trung_binh'] = fuzzy.trimf(priority.universe, [3, 5, 7])
priority['cao'] = fuzzy.trimf(priority.universe, [6, 10, 10])

rules = [
    ctrl.Rule(density['cao'] & load['thap'] & traffic['thap'], combine['nhieu']),
    ctrl.Rule(density['trung_binh'] & traffic['cao'] & urgency['trung_binh'], combine['mot_so']),
    ctrl.Rule(load['cao'] & density['cao'] & profit['trung_binh'], combine['mot_so']),
    ctrl.Rule(density['thap'] & urgency['cao'] & traffic['trung_binh'], combine['mot_so']),
    ctrl.Rule(profit['cao'] & urgency['cao'] & traffic['cao'], combine['mot_so']),
    ctrl.Rule(urgency['cao'] & profit['cao'], priority['cao']),
    ctrl.Rule(urgency['trung_binh'] & traffic['trung_binh'], priority['trung_binh']),
    ctrl.Rule(urgency['thap'] & density['cao'], priority['thap'])
]

log_sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

print("----- NHẬP DỮ LIỆU LOGISTICS -----")
try:
    log_sim.input['density'] = float(input("Mật độ đơn hàng (0-10): "))
    log_sim.input['urgency'] = float(input("Mức khẩn cấp (0-10): "))
    log_sim.input['load'] = float(input("Tải trọng hiện tại (0-10): "))
    log_sim.input['traffic'] = float(input("Tình trạng giao thông (0-10): "))
    log_sim.input['profit'] = float(input("Lợi nhuận dự kiến (0-10): "))

    log_sim.compute()
    print(f"\n=> Nên kết hợp: {log_sim.output['combine']:.2f} đơn")
    print(f"=> Độ ưu tiên giao hàng: {log_sim.output['priority']:.2f}/10")
except:
    print("Lỗi nhập liệu!")