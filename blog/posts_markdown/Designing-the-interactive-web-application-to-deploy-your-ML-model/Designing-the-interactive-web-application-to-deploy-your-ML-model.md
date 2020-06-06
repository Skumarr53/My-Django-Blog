

<img class="ef so s t u dq ai ip" width="960" height="594" srcset="https://miro.medium.com/max/552/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 276w, https://miro.medium.com/max/1104/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 552w, https://miro.medium.com/max/1280/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 640w, https://miro.medium.com/max/1400/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/864/1*h5Zp7_iQM4CGRQI_fN-iwg.gif">

<center><i>application predicts the price of used car</i></center>

<br>
In this tutorial, let's work towards creating a web application out of the machine learning model we built in python using Flask. For demonstration purposes, I am using a model of my own that predicts the price of used cars in major cities of India. Dataset used here is from a hackathon hosted by [MachineHack](https://www.machinehack.com/). Go to the hackathon [homepage](https://www.machinehack.com/course/predicting-the-costs-of-used-cars-hackathon-by-imarticus/) to know more about the dataset. Dataset set contains features like Location, Manufacture details, car features such as Fuel type, Engine, and usage parameters. For understanding, web application development some basic knowledge of **HTML** and **JQuery** is useful but not mandatory. I will try my best to explain as we go along.  

I encourage you to look at files as I go along explaining things. Go to this [git repository](https://github.com/Skumarr53/predicting-the-costs-of-used-cars) and download the *webApp* folder to your local. Please refer to the ```PricePredictions_UsedCars.ipynb``` to understand featurization and model selection pipeline.


For deploying the ML model I am using the **Flask** web development framework. Web application setup mainly contains two files
1. Application.py - python script that handles routing and preforms computation in the backend.

2. index.html - HTML file that acts as a GUI interface between client and server. It allows users to submit inputs and transfers them to application.py for computation and renders output on the interface.

explains variables and types

Input files used into *Flask* application:
1. GBM_Regressor_pipeline.pkl - pickle object that encodes all the preprocessing, feature transformation, and model trained model parameters. Sklearn's **pipeline** is a great way to store work-flow for reproducibility as in this case. Raw inputs from users passed into the pipeline which applies transformations and then predicts price.  

2. Encoded_dicts.pkl - As I mentioned, there are categorical variables we need to pass mappings along with the encoded values. This pickle object that stores labels and encodes mappings for categorical variables.

3. model2brand.pkl - pickle object that stores dictionary of the brand and models mappings i.e **brand** as *key* and list of car models belong to that brand as *value*. This is used to filter models for user-selected **brand**.


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
```@application.before_first_request``` is the decorator that calls function ```startup``` when the server is started or before any request has been placed. The function loads all the inputs into the app.

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

```@application.route``` decorator calls ```background_process``` API, whenever route is requested (*'/background_process'* in this case). This function either uses default inputs ('GET' method) or retrieves inputs from request objects ('POST' method), predicts based on these inputs and outputs prediction in JSON format.

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

The core purpose which *index.html* has to serve is getting user arguments from the client-side and pass them to *application.py* script for processing. We need to create interactive elements that make it easy for the user to submit inputs.

For collecting numerical inputs, let's use *slider* objects and for categorical inputs, it is appropriate to use *dropdown* object.

### Slider object

I am taking an example of *slider* HTML snippet and understand what's happening.

``` html
<div class="slidecontainer">
    <label> Year: <span id="Year"></span></label>
    <input type="range" min="1998" max="2019" value="2014" class="slider" id="year_range" step="1">
</div>
```

* ```div``` tag separates objects within it from other elements. It's always preferable to use it.
* ```span``` tag allows user to continue text in the same line but wants highlight text in some way like highlighting by color
* ```label``` tag is used to indicate user what field he is providing input for (*Year* in this case).
* ```input``` tag is the one that receives input from the user. The *min* and *max* attributes decide range, *value* holds current selection by the user, *class* tells what of object (*slider*  in this case) and *step* decides step size.

Note: ```id``` attribute in each tag is important as they serve as unique identifiers for objects or tags, therefore, no two tags should have the same *id*.

#### Making Slider object interactive

Now that we have created *slider* object that allows users to select a value between a certain range. To let the user know what *value* he has selected we can pass the value inside *span* tag. Let see how this is done.

```java
var slider3 = $("#year_range");
$("#Year").html(slider3.val());
```

the above snippet is Jquery script (a proxy of javascript that makes simple to code).

What this snippet does is:
* Creates a variable *slider3* and assigns tag with *year_range* as id (year input tag in this case). Now that we assigned we can modify or retrieve information from this tag.

* We are interested *value* attribute of the tag selected as it holds user selected year. ```slider3.val()``` fetches this value and passes it inside *html()*  in the ```$("#Year").html()``` making it appear inside of the tag with id *Year* (*span* tag in this case) as text after "Year: ".

Now, all we did is to read *value* attribute from input tag and pass it along inside *label* tag. But, right now the object is not capable of recording other than the default value (provided by us) i.e user-provided values by moving slider. To do that we have to make objects detect *slider* movement.

``` java
slider3.change(function() {
    $("#Year").html(slider3.val());
})
```
```slider3.change()``` detects slider movement and then calls ```function()``` that does same as the above one expect this and updates text inside *label* tag making it interactive.

<!DOCTYPE html>
<body>
    <div class="slidecontainer">
        <label> Year: <span id="Year">
        </span></label>
        <input type="range" min="1998" max="2019" value="2014" class="slider" id="year_range" step="1">


### Dropdown object

Now let's pick a dropdown object and understand how to make it work. As I already mentioned *dropdown* is used for categorical variables where the user selects an option and this option needs to be mapped to the number representing it, unlike *slider* object where the user input value is directly passed for model prediction. 

To achieve that we need to have mapping python dictionaries as well for each categorical variable. Let us understand how we can create a dropdown that allows users to submit input.

``` html
<div class="dropdownlist">
    <label for="brand">Choose a Brand: <span><select id="brand"></select></span></label>                        
</div>
```

The ```select``` tag in the above HTML snippet creates an empty dropdown list. To fill a dropdown with options, we need to use ```option``` tag inside ```select``` tag. But, what if we have a lot of options to fill in making this job cumbersome. In such a case, we can iterate the python dictionary with *brand* and label encode mappings like the one shown below with JQuery.

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
The above code creates a variable ```brands``` that stores *le_brands_Encdict* dictionary passed to template from application.py. while iterating dictionary *keys* it gets corresponding encoded value stores in variable ```value``` appends ```option``` inside the tag with id *brand* (```select``` tag in this case) filling the dropdown with options.  

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

``` java
$('#brand option:selected').html()
```

the line above fetches the **brand** the user has selected. 


Using the discussed approach we need *slider* and *dropdown* objects for the rest of the variables.

## Passing user inputs to the function
Till now we have discussed how we could get user input in the background we need to pass those to  ```background_process()``` function that predicts price.


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

Let's go through the above code snippet. ```$(document).mouseup()``` and ```$(document).on``` are the event listeners that captures mouse clicks and drop down changes respectively, then calls ```fetchdata()``` function that routes to ```url_for('background_process')``` calling ```background_process``` API. The *data* argument inside the function collects inputs from all the objects and passes them to ```background_process``` function as arguments and outputs a *json* object *price_prediction* as key and predicted price as value.

Upon successful ```success: function(data)``` takes this *json* object and then passes predicted value ```data.price_prediction``` to the  ```update_dashboard``` function which in turn passes it to the tag with id ```estimated_price``` (```label``` tag in this case) displaying the price on the web page.
