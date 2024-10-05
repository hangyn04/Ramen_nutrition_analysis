import requests
import pandas as pd
import json

app_id = 'd12ac0ad'
app_key = '1d6ab8a57612d8de2d152e99cbd96775'

api_url = 'https://trackapi.nutritionix.com/v2/search/instant'

def get_ramen(query):
    params = {
        'query': query,
        'branded': 'true',
        'detailed': 'true'
    }

    headers = {
        'x-app-id': app_id,
        'x-app-key': app_key
    }

    response = requests.get(api_url, headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    return data

#queries = ['Shin Noodle Soup Ramen', 'Maruchan', 'Buldak ramen', 'Indomie', 'Nongshim', 'Nissin', 'Ichiban', 'Chef Woo', 'Jinya', 'Menraku', 'Samyang']

queries = ['ramen','Ramen', 'Noodles','noodles']

product_names = []
brands = []
calories = []
total_fat = []
sodium = []
carbohydrates = []
proteins = []
serving_sizes_in_grams = []
serving_sizes_in_pack = []

for query in queries:
    data = get_ramen(query)
    for item in data.get('branded'):
        product_name = item.get('food_name', 'N/A')
        brand_name = item.get('brand_name', 'N/A')
        serving_size = item.get('serving_qty', 'N/A')  # Extract serving size
        serving_unit = item.get('serving_unit', '')    # Extract serving unit (e.g., g, oz)
        serving_size_str = f"{serving_size} {serving_unit}" if serving_size != 'N/A' else 'N/A'

        # Extract serving size in grams
        serving_size_in_g = item.get('serving_weight_grams', 'N/A')

        # Initialize variables for nutritional values
        p_calories = 'N/A'
        p_total_fat = 'N/A'
        p_sodium = 'N/A'
        p_protein = 'N/A'
        p_carbohydrates = 'N/A'

        # Extract detailed nutritional information from 'full_nutrients'
        if 'full_nutrients' in item:
            nutrients = item['full_nutrients']
            for nutrient in nutrients:
                attr_id = nutrient.get('attr_id')
                value = nutrient.get('value')
                if attr_id == 208:  # Calories
                    p_calories = value
                elif attr_id == 204:  # Total Fat
                    p_total_fat = value
                elif attr_id == 307:  # Sodium
                    p_sodium = value
                elif attr_id == 203:  # Protein
                    p_protein = value
                elif attr_id == 205:  # Carbohydrates
                    p_carbohydrates = value

        # Append data to lists
        product_names.append(product_name)
        brands.append(brand_name)
        serving_sizes_in_grams.append(serving_size_in_g)
        serving_sizes_in_pack.append(serving_size_str)
        calories.append(p_calories)
        total_fat.append(p_total_fat)
        sodium.append(p_sodium)
        proteins.append(p_protein)
        carbohydrates.append(p_carbohydrates)

# Create a DataFrame to store the scraped data
ramen_data = pd.DataFrame({
    'Product Name': product_names,
    'Brand': brands,
    'Serving_Size': serving_sizes_in_pack,
    'Serving_Size_in_(g)': serving_sizes_in_grams,
    'Calories': calories,
    'Total Fat (g)': total_fat,
    'Sodium (mg)': sodium,
    'Protein (g)': proteins,
    'Carbohydrates (g)': carbohydrates,
})

# Display the DataFrame
print(ramen_data)
#print(ramen_data['Serving_Size_in_(g)','Calories','Serving_Size'])
#print(ramen_data.iloc[:, [2,3,4]])

# Save the DataFrame to a CSV file
#ramen_data.to_csv('C:/Users/Ha/Desktop/Research/ramen_nutrition.csv', index=False)

