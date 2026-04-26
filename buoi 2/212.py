import numpy as np
import skfuzzy as fuzzy
from skfuzzy import control as ctrl

rating = ctrl.Antecedent(np.arange(0, 6, 0.1), 'rating')
sales = ctrl.Antecedent(np.arange(0, 1001, 1), 'sales')
margin = ctrl.Antecedent(np.arange(0, 101, 1), 'margin')
event = ctrl.Antecedent(np.arange(0, 11, 1), 'event')
competitor = ctrl.Antecedent(np.arange(0, 11, 1), 'competitor')
discount = ctrl.Consequent(np.arange(0, 71, 1), 'discount')

rating['thap'] = fuzzy.trimf(rating.universe, [0, 0, 4])
rating['trung_binh'] = fuzzy.trimf(rating.universe, [4, 4.25, 4.5])
rating['cao'] = fuzzy.trimf(rating.universe, [4.5, 5, 5])
sales['thap'] = fuzzy.trimf(sales.universe, [0, 0, 300])
sales['trung_binh'] = fuzzy.trimf(sales.universe, [200, 500, 800])
sales['cao'] = fuzzy.trimf(sales.universe, [700, 1000, 1000])
margin['thap'] = fuzzy.trimf(margin.universe, [0, 0, 30])
margin['trung_binh'] = fuzzy.trimf(margin.universe, [20, 50, 80])
margin['cao'] = fuzzy.trimf(margin.universe, [70, 100, 100])
event['khong'] = fuzzy.trimf(event.universe, [0, 0, 3])
event['trung_binh'] = fuzzy.trimf(event.universe, [2, 5, 8])
event['cao'] = fuzzy.trimf(event.universe, [7, 10, 10])
competitor['thap'] = fuzzy.trimf(competitor.universe, [0, 0, 5])
competitor['cao'] = fuzzy.trimf(competitor.universe, [5, 10, 10])
discount['rat_thap'] = fuzzy.trimf(discount.universe, [0, 0, 5])
discount['thap'] = fuzzy.trimf(discount.universe, [5, 7.5, 10])
discount['trung_binh'] = fuzzy.trimf(discount.universe, [10, 15, 20])
discount['cao'] = fuzzy.trimf(discount.universe, [20, 30, 40])
discount['rat_cao'] = fuzzy.trimf(discount.universe, [40, 55, 70])

rules = [
    ctrl.Rule(rating['cao'] & sales['cao'] & margin['cao'], discount['rat_thap']),
    ctrl.Rule(rating['thap'] & sales['thap'] & margin['cao'], discount['cao']),
    ctrl.Rule(event['cao'] & competitor['cao'], discount['rat_cao']),
    ctrl.Rule(rating['trung_binh'] & sales['trung_binh'] & margin['trung_binh'], discount['trung_binh']),
    ctrl.Rule(competitor['thap'] & margin['thap'] & sales['cao'], discount['rat_thap']),
    ctrl.Rule(rating['thap'] & event['khong'], discount['trung_binh']),
    ctrl.Rule(sales['thap'] & margin['thap'], discount['rat_cao'])
]

shopee_sim = ctrl.ControlSystemSimulation(ctrl.ControlSystem(rules))

print("----- NHẬP DỮ LIỆU SHOPEE -----")
try:
    shopee_sim.input['rating'] = float(input("Nhập đánh giá shop (1-5 sao): "))
    shopee_sim.input['sales'] = float(input("Nhập doanh số bán hàng (đơn/tháng): "))
    shopee_sim.input['margin'] = float(input("Nhập biên lợi nhuận (%): "))
    shopee_sim.input['event'] = float(input("Sự kiện mùa (0:Không - 10:Cao): "))
    shopee_sim.input['competitor'] = float(input("Chiết khấu đối thủ (0:Thấp - 10:Cao): "))

    shopee_sim.compute()
    print(f"\n=> Mức chiết khấu đề xuất: {shopee_sim.output['discount']:.2f}%")
except:
    print("Lỗi nhập liệu!")