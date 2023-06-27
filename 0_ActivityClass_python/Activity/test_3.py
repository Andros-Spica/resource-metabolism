import Activity
import matplotlib.pyplot as plt

# Define the input values for the activity
labor = 10
land = 20
stocks = [{"wood": 100, "stone": 50, "axe": 0, "hammer": 0}]

# Create instances of the Activity class
mining_stone = Activity.Activity("stone")
woodcutting = Activity.Activity("wood")
toolMaking_axe = Activity.Activity("axe")
toolMaking_hammer = Activity.Activity("hammer")

# production chain

numWorkingDays = 10

for day in range(numWorkingDays):

    print('~~~~~~ Day ' + str(day) + ' ~~~~~~')

    stocks.append(stocks[day])
    stocks[day + 1] = mining_stone.perform(labor, land, stocks[day + 1], verbose=True)
    stocks[day + 1] = woodcutting.perform(labor, land, stocks[day + 1], verbose=True)
    stocks[day + 1] = toolMaking_axe.perform(labor, land, stocks[day + 1], verbose=True)
    stocks[day + 1] = toolMaking_hammer.perform(labor, land, stocks[day + 1], verbose=True)

# plot change in stocks

materialColors = {"wood": 'brown', "stone": 'grey', "axe": 'violet', "hammer": 'orange'}

# Extract the keys and values into separate lists
keys = list(stocks[0].keys())
values = [[dictionary[key] for key in keys] for dictionary in stocks]

fig, ax = plt.subplots()
for i in range(len(keys)):
    ax.plot(range(len(stocks)), [values[j][i] for j in range(len(stocks))], label=keys[i])
ax.legend()

# Save the plot as a png file
plt.savefig('line_plot.png')