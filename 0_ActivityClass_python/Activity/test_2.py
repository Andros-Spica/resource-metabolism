import Activity

# Define the input values for the activity
labor = 10
land = 20
stocks = {"wood": 100, "stone": 50, "water": 0} # unused input does not affect the result

# Create two instances of the Activity class
toolMaking_axe = Activity.Activity("axe")
toolMaking_hammer = Activity.Activity("hammer")

# Print activity configuration
toolMaking_axe.print_configuration()
toolMaking_hammer.print_configuration()

# Calculate output per each of the selected output for the activity (assuming same inputs)
newStock = toolMaking_axe.perform(labor, land, stocks, verbose=True)

# Calculate output per each of the selected output for the activity (assuming same inputs)
newStock = toolMaking_hammer.perform(labor, land, newStock, verbose=True)

print(newStock)