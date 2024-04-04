from fastapi import FastAPI
import json
app = FastAPI()





@app.get('/all_products/')
def root():
    context= {}
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        for key,value in data.items():
            context[key] = data[key]['name']
    return context
            

@app.get('/products/{product_pk}/')
def product_info(product_pk):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        context = data[f'{product_pk}']
    return context

@app.get('/products/{product_pk}/{product_field}')
def product_field_info(product_pk:int,product_field:str):
    with open('data.json', 'r') as json_file:
        data = json.load(json_file)
        context = data[f'{product_pk}'][f'{product_field}']
    return context