import pandas as pd
import matplotlib.pyplot as plt

def cost(sales):
    inventory_cost = sales * 0.25
    staffing_need = sales / 80000
    staffing_cost = staffing_need * 5000
    total_cost = inventory_cost + staffing_cost
    return [inventory_cost, staffing_need, staffing_cost, total_cost]

sales = [30000,50000,70000,90000,110000]
stats = []
for sale in sales:
    result = cost(sale)
    stats.append(result)

results_table = pd.DataFrame(stats, columns=["Inventory Cost", "Staffing Need", "Staffing Cost", "Total Cost"])
results_table["Sales Forecast"] = sales
plt.figure(figsize = (8,5))
plt.plot(results_table["Sales Forecast"], results_table["Inventory Cost"], label = "Inventory Cost")
plt.plot(results_table["Sales Forecast"], results_table["Staffing Cost"], label = "Staffing Cost")
plt.plot(results_table["Sales Forecast"], results_table["Total Cost"], label = "Total Cost")
plt.xlabel("Sales Forecast")
plt.ylabel("Cost")
plt.title("Sales Forecast")
plt.legend()
plt.savefig("sales_forecast.png")


 

