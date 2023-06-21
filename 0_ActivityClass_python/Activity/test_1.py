import Activity

# Define the input values for the activity
labor = 10
land = 20
stocks = {"wood": 100, "stone": 50}

# Create an instance of the Activity class
activity = Activity.Activity("axe")

# Print activity configuration
activity.print_configuration()

# Calculate output for the activity
newStock = activity.perform(labor, land, stocks, verbose=True)

print(newStock)