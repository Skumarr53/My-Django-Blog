

In this article, I will share my experience in creating an interactive web application out of the ML model using the Flask framework. For demonstration purposes, I am using a model of my own that predicts the price of used cars in major cities of India. Dataset used here is from a hackathon hosted by [MachineHack](https://www.machinehack.com/). Go to the hackathon [homepage](https://www.machinehack.com/course/predicting-the-costs-of-used-cars-hackathon-by-imarticus/) to know more about the dataset. Dataset set contains features like Location, Manufacture details, car features such as Fuel type, Engine, and usage parameters. To understand the code some basic knowledge of HTML and JQuery is useful but not mandatory. I will try my best to explain as we go along. Have a glance at the working application.

<img class="ef so s t u dq ai ip" width="960" height="594" srcset="https://miro.medium.com/max/552/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 276w, https://miro.medium.com/max/1104/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 552w, https://miro.medium.com/max/1280/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 640w, https://miro.medium.com/max/1400/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/864/1*h5Zp7_iQM4CGRQI_fN-iwg.gif">

<center><i>application predicts the price of used car</i></center></br>

I encourage you to look at files as I go along explaining things. Go to this [git repository](https://github.com/Skumarr53/predicting-the-costs-of-used-cars) and download the *webApp* folder to your local. Please refer to the ```PricePredictions_UsedCars.ipynb``` if you want to understand the featurization and model selection pipeline.


This application is developed using the **Flask** web development framework. Web application setup contains two files
1. Application.py - python script that handles routing and preforms computation in the backend.

2. index.html - HTML file that acts as a GUI interface between client and server. It allows users to submit inputs and transfers them to application.py for computation and renders output on the interface.

Other python objects used in *Flask* application:
1. **GBM_Regressor_pipeline.pkl** - Pickle object that encodes all the preprocessing, feature transformation, and model trained model parameters. Sklearn's **pipeline** is a great way to store work-flow for reproducibility as in this case. Raw inputs from users passed into the pipeline which applies transformations and then predicts price.  

2. **Encoded_dicts.pkl** - There are categorical variables in featuers. we need to pass them along with the encoded numerical values. This pickle object stores mapping hash table.

3. **model2brand.pkl** -  *Model* feature is partially dependent on the *Brand* feature. Dependent in the sense a set of models are unique to a particular brand. When a user selects a brand, only the models that belong to the selected brand should appear in model selection dropdown object (```choose a model```). To make it possible, we need to store a dictionary of the brand and models set mappings i.e brand as *key* and set of car models belong to that brand as *value*. This is used to filter models for the user-selected brand.


``` python
{'Fiat': ['Siena', 'Punto', 'Avventura', 'Grande', 'Petra', 'Linea']}
```

## Explore the contents in *Application.py* 

Importing required libraries
``` python
from flask import (Flask, render_template, flash,
                    request, jsonify, Markup)
import logging, io, os, sys
import pandas as pd
import numpy as np
from modules.custom_transformers import *
from sklearn.ensemble import GradientBoostingRegressor
import scipy
import pickle
```

### Loading inputs 

``` python
@application.before_first_request
def startup():

    global gbm_model, model2brand
    
    # gbm model
    with open('../gbm_model_dump.pkl', 'rb') as f:
        gbm_model = pickle.load(f)

    # Encoded values to categories mapping dictionary
    with open('../Encoded_dicts.pkl', 'rb') as f:
        le_brands_Encdict,le_models_Encdict,le_locations_Encdict,le_fuel_types_Encdict,le_transmissions_Encdict,le_owner_types_Encdict = pickle.load(f)

    with open('../model2brand.pkl', 'rb') as f:
        model2brand = pickle.load(f)
```

```@application.before_first_request``` is the decorator that calls the function ```startup``` when the server starts. The function loads all the python objects.

``` python
@application.route('/background_process', methods=['POST', 'GET'])
def background_process():
    Brand = request.args.get('Brand')                                        
    Model = request.args.get('Model')                                        
    Location = request.args.get('Location')
    Year = int(request.args.get('Year'))                                          
    Kilometers_Driven = float(request.args.get('Kilometers_Driven'))                
    Fuel_Type = request.args.get('Fuel_Type')
    Transmission = request.args.get('Transmission')
    Owner_Type = request.args.get('Owner_Type')
    Mileage = float(request.args.get('Mileage'))                                    
    Engine = float(request.args.get('Engine'))                                      
    Power = float(request.args.get('Power'))                                        
    Seats = float(request.args.get('Seats'))

	# values stored in the list later to be passed as df while prediction
    user_vals = [Brand, Model, Location, Year, Kilometers_Driven, 
        Fuel_Type, Transmission, Owner_Type, Mileage, Engine, 
        Power, Seats]


    x_test_tmp = pd.DataFrame([user_vals],columns = features)

    pred = gbm_model.predict(x_test_tmp[features]).tolist()
    return jsonify({'price_prediction':pred})
```

```@application.route``` decorator calls ```background_process``` API, whenever this route is requested. This function uses default inputs ('GET' method) when page is loaded and retrieves inputs from request objects ('POST' method) as well. This funtion compute price based on provided inputs and outputs prediction in ```JSON``` format.

finally,
``` python
@application.route("/", methods=['POST', 'GET'])
def index():
     # Encoded values to categories mapping dictionary
    with open('../Encoded_dicts.pkl', 'rb') as f:
        le_brands_Encdict,le_models_Encdict,le_locations_Encdict,le_fuel_types_Encdict,le_transmissions_Encdict,le_owner_types_Encdict = pickle.load(f)

    return render_template( 'index.html', model2brand = model2brand,le_models_Encdict = le_models_Encdict,le_locations_Encdict = le_locations_Encdict, le_fuel_types_Encdict = le_fuel_types_Encdict, le_transmissions_Encdict = le_transmissions_Encdict, le_owner_types_Encdict = le_owner_types_Encdict, le_brands_Encdict = le_brands_Encdict,price_prediction = 17.09)

```

Renders *index.html* and Also pass other arguments to be used inside the template (dictionaries in this case).

## Explore Contents in Index.html

The core purpose of *index.html* is to get user arguments from the client-side and pass them to *application.py* script for processing and retrieve prediction. We need to create interactive elements that make it easy for the user to submit inputs.

As we noticed we have both numerical and categorical features. For collecting numerical inputs, I will use *slider* objects and for categorical inputs, it is appropriate to use *dropdown* objects.

### Slider object

Let's take a slider object ```HTML``` snippet and understand what's happening.

``` html
<div class="slidecontainer">
    <label> Year: <span id="Year"></span></label>
    <input type="range" min="1998" max="2019" value="2014" class="slider" id="year_range" step="1">
</div>
```

* ```div``` tag separates objects within it from other elements. It's always preferable to separate objects from each other.

* ```label``` tag used to show the user what field he is providing input for (variable is *Year* in this case).

* ```span``` tag allows us to highlight part of the text enclosed within ```label``` tag. Only the text inside this tag can be highlighted(right now it is empty). 

* ```input``` tag is the one that receives input from the user. The *min* and *max* attributes decide slider range, *value* attribute holds selected value by the user, *class* the tells type of object (*slider*  in this case) and *step* decides step size of slider movement.

Note: ```id``` attribute in each tag is important as it serves as a unique identifier of objects or tags, therefore, no two tags should have the same *id*.

#### Making Slider object interactive

Now that we have created a *slider* object which allows the user to select a value between a certain range. To let the user know what *value* he has selected we can pass the selected value inside the *span* tag. Let see how it's done.

```java
var slider3 = $("#year_range");
$("#Year").html(slider3.val());
```

the above snippet is Jquery script (a proxy of javascript that makes simple to code).

What this snippet does is:

* It creates a *slider3* variable which tag element with attribute```id=year_range```. This allows us to retrieve or modify attribute values.

* As we are interested user-selected value stored in the *value* attribute. ```slider3.val()``` fetches this value and passing it inside *html()*  in the ```$("#Year").html()``` as text making it appear inside the tag with ```id=Year``` (*span* tag inside Year ```label``` tag).

Now, all we did is to read the *value* attribute from input tag and pass it along inside the *label* tag. But, right now the object is not capable of recording other than the default value (provided by us). We need to make it detect slider movement and read the corresponding user-selected value.

``` java
slider3.change(function() {
    $("#Year").html(slider3.val());
})
```

```slider3.change()``` detects slider movement of ```slider3``` object and then calls ```function()``` that does the same as the above one except and updates text inside *label* tag making it interact with slider object.

### Dropdown object

As I already mentioned, the **dropdown** object is used for categorical variables where the user selects an option and this option needs to be mapped to the numerical value, unlike **slider** objects where the user input value is directly passed for model prediction. To achieve this, we need to have mapping python dictionaries.

below is the mapping hash table for the variable brand.

``` python
{'Ambassador': 0,
 'Audi': 1,
 'BMW': 2,
 'Bentley': 3,
 'Chevrolet': 4,
 'Datsun': 5,
 'Fiat': 6,
 'Force': 7,
 'Ford': 8,
 'Hindustan': 9,
 'Honda': 10,
 'Hyundai': 11,
 'ISUZU': 12,
 'Isuzu': 13}
```

Let us understand how we can create a dropdown allowing users to pass input.

``` html
<div class="dropdownlist">
    <label for="brand">Choose a Brand: <span><select id="brand"></select></span></label>                        
</div>
```

The ```select``` tag in the above **HTML** snippet creates an empty dropdown list. To fill a dropdown with possible options, we use ```option``` tag inside ```select``` tag to store keys. But, what if we have a lot of keys to fill in which makes this job cumbersome. In such a case, we can iterate the dictionary keys.

``` java
var brands = {{ le_brands_Encdict|safe }}
for (let key in brands) {
    i=0;
    let value = brands[key];
    //alert( value);
    $('#brand').append('<option value=' + value + '>' + key + '</option>');
    i++;
    }
```
The above code creates a variable ```brands``` that stores *le_brands_Encdict* dictionary passed by ```index()``` function from **application.py**. while iterating dictionary *keys* it fetches *value* stores in variable ```value``` and then passes it inside a ```option``` tag created along with the *key*.

```option``` tags appended inside the ```select``` tag with ```id=brand``` filling the dropdown with options.

<div class="dropdownlist">
    <label for="brand">Choose a Brand: <span>
    <select id="brand">                        

<option value="0">Ambassador</option>
<option value="1">Audi</option>
<option value="2">BMW</option>
<option value="3">Bentley</option>
<option value="4">Chevrolet</option>
<option value="5">Datsun</option>
<option value="6">Fiat</option>
<option value="7">Force</option>
<option value="8">Ford</option>
</select>
</div>
<br>


below **Jquery** snippet fetches the **brand** the user has selected from dropdown options.

``` java
$('#brand option:selected').html()
```

I have explained taking two objects as reference (**year** for numerical and **brand** for categorical). we have similar objects for the rest of the variables.

## Passing user inputs to the function
Till now we have discussed how we could get user inputs in the background. Now, we have to pass those to  ```background_process()``` function that computes price.


``` javascript
// functions for updating predictions
function update_dashboard(price_prediction){
    $('#estimated_price').html(price_prediction);
    }

function fetchdata()
{
// dictionary that stores user inputs
    $.getJSON({
        type: "GET",
        url: '{{ url_for('background_process') }}',
        data: {
            'Brand': $('#brand option:selected').html(),
            'Model': $('#Model option:selected').html(),
            'Location': $("#Location option:selected").html(),
            'Year': $("#Year").html(),
            'Kilometers_Driven': $("#km_drive").html(),
            'Fuel_Type': $("#Fuel_type option:selected").html(),
            'Transmission': $("#Transmission option:selected").html(),
            'Owner_Type': $("#Owner_type option:selected").html(),
            'Mileage': $("#Mileage").html(),
            'Engine': $("#Engine").html(),
            'Power': $("#Power").html(),
            'Seats': $("#Seats").html(),
        },
        success: function(data){
            logger = data.price_prediction
            update_dashboard(data.price_prediction);
        }
    });
}

// add event listener to capture changes to wine parameters  
$(document).mouseup(function () {fetchdata()});
$(document).on('change', function () {fetchdata()});

```

Let's go through the above code snippet. ```$(document).mouseup()``` and ```$(document).on``` are the event listeners that captures mouse clicks and drop-down changes respectively, then calls ```fetchdata()``` function that routes to ```url_for('background_process')``` calling ```background_process``` API (refer to application.py file). The *data* argument inside the function collects user inputs from all the objects and passes them to ```background_process``` function as arguments that compute price and then output a **JSON** object. The output **JSON** object has *key* ```price_prediction```   and price computed is *value*.

Upon successful ```success: function(data)``` takes *JSON* object and then passes predicted value to the  ```update_dashboard``` function which in turn passes it to the tag with ```id = estimated_price``` (price ```label``` tag) displaying the predicted price on the web page.

Thank you for reading.
