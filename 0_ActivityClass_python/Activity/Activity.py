import math
import json

class Activity:
    def __init__(self, output_type):
        self.output_type = output_type

        output_data = get_material_data(output_type)

        self.production_function = output_data['production_function']
        self.max_productivity_per_input_good = output_data['max_productivity_per_input_good']
        self.max_productivity_per_labor = output_data['max_productivity_per_labor']
        self.max_productivity_per_land = output_data['max_productivity_per_land']
        self.output_step_amount = output_data['step_amount']
        
        self.input_types = self.get_input_types()
        self.input_step_amounts = self.get_input_step_amounts()

    def get_input_types(self):
        return self.max_productivity_per_input_good.keys()
    
    def get_input_step_amounts(self):
        input_step_amounts = dict()
        for input_type in self.max_productivity_per_input_good.keys():
            input_step_amounts[input_type] = get_material_data(input_type)['step_amount']
        return input_step_amounts

    # Method for printing out the input and output values for the activity
    def print_configuration(self):
        print(f"Activity output: {self.output_type}")
        print(f"Input types: {self.input_types}")
        print(f"Production functions: {self.production_function}")
        print(f"Max. productivity per input good: {self.max_productivity_per_input_good}")
        print(f"Max. productivity per labor: {self.max_productivity_per_labor}")
        print(f"Max. productivity per land: {self.max_productivity_per_land}")
    
    def perform(self, labor, land, available_input_goods, verbose=False):
        if (verbose):
            print(f"Activity output: {self.output_type}")
            print(f"Input: labor={labor}, land={land}, goods={available_input_goods}")

        production_formula = self.production_function
        max_output_per_input_type = {}
        for input_good, conversion_rate in self.max_productivity_per_input_good.items():
            if input_good not in available_input_goods:
                raise Warning(f"No output is possible because {input_good} is missing")
                return 0
            max_output_per_input_type[input_good] = conversion_rate * available_input_goods[input_good]
        max_output_per_input_type["labor"] = labor * self.max_productivity_per_labor
        max_output_per_input_type["land"] = land * self.max_productivity_per_land
        for input_name, input_value in max_output_per_input_type.items():
            if not isinstance(input_value, (int, float)):
                raise ValueError(f"Invalid input type for {input_name}: {type(input_value)}")
            if input_value < 0:
                raise ValueError(f"Invalid input value for {input_name}: {input_value}")
        
        output_amount = self.calculate_max_output(production_formula, max_output_per_input_type)
        output_amount = floor_to_step(output_amount, self.output_step_amount)
        if (verbose): print(f"Output: {self.output_type}={output_amount}")

        unused_input_goods = dict()
        for input_good, input_amount in available_input_goods.items():
            if input_good not in self.max_productivity_per_input_good:
                unused_input_goods[input_good] = input_amount
            else:
                unused_input_goods[input_good] = input_amount - (output_amount / self.max_productivity_per_input_good[input_good])
                unused_input_goods[input_good] = ceiling_to_step(unused_input_goods[input_good], self.input_step_amounts[input_good])

        full_collection_of_goods = unused_input_goods
        if self.output_type not in unused_input_goods:
            full_collection_of_goods[self.output_type] = output_amount
        else:
            full_collection_of_goods[self.output_type] += output_amount

        return full_collection_of_goods
    
    def calculate_max_output(self, production_formula, inputs):
        max_output = eval(production_formula, {}, inputs)
        if max_output < 0:
            raise ValueError("Invalid output value")
        return max_output

def floor_to_step(value, step):
    return math.floor(value/step) * step

def ceiling_to_step(value, step):
    return math.ceil(value/step) * step

def get_material_data(name):
    with open('Materials.json') as f:
            materials_data = json.load(f)
    data = [entry for entry in materials_data if entry['name'] == name]
    if len(data) == 0: raise ValueError("There are no entry in 'Materials.json' matching output_type.")
    if len(data) > 1: raise ValueError("There are more than one entry in 'Materials.json' matching output_type.")
    data = data[0]
    return data