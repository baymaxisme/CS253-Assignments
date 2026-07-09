def calculate_raw_materials(item, quantity, recipes):
    #if the item is not in recipes than it is a raw material
    if item not in recipes:
        return {item : quantity}
    
    #dictionary of ingredients for 1 unit of given item
    ingredient_needed = recipes[item]

    #Dictionary to store the raw materials used in the item
    raw_materials = {}

    for ingredient, amount_per_unit in ingredient_needed.items():

        #Total quantity needed of the particular ingredient in making of the item 
        total_needed = quantity*amount_per_unit

        #Breaking down the particular ingredient into its raw materials
        sub_materials = calculate_raw_materials(ingredient, total_needed, recipes)

        #Merging the sub_materials into the main raw_materials dictionary
        for material_name, material_quantity in sub_materials.items():
            if material_name in raw_materials:
                raw_materials[material_name] += material_quantity
            else:
                raw_materials[material_name] = material_quantity

    return raw_materials

#TO SEE OUTPUT
#if __name__ == "__main__":
#   recipes = {
#       'SteelSword': {'SteelIngot': 2, 'LeatherGrip': 1},
#        'SteelIngot': {'IronOre': 3, 'Coal': 2},
#        'LeatherGrip': {'Leather': 1, 'String': 2},
#        'String': {'PlantFibers': 3}
#    }
#
#    print(calculate_raw_materials('SteelSword', 5, recipes))
