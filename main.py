from fastapi import FastAPI
import json
app = FastAPI()





@app.get('/all_products/')
def root():
    context= {}
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        for key in data:
            context[key] = data[key]['name']
    return context
            

@app.get('/products/{product_name}/')
def product_info(product_name:str):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        context = data[product_name]
    return context

@app.get('/products/{product_name}/{product_field}')
def product_field_info(product_name:str,product_field:str):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        context = data[product_name][product_field]
    return context