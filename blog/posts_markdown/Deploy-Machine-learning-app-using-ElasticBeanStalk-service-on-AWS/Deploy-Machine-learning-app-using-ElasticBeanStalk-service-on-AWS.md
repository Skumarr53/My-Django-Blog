
 To deploy a model, we should build one, which is obvious. the model ready to be deployed must be exported in ```.pkl``` file, a python object which the web development framework like **Flask** expects. Since you are here to learn deployment I assume you have your app ready for deployment, if not, you may use my sample app from this [repository](https://github.com/Skumarr53/Used-Car-Price-Prediction/tree/master/webApp). Please refer to the ```PricePredictions_UsedCars.ipynb``` to understand featurization and model selection pipeline.

 #### Short description of my ML model<br>
 
 The model predicts the price of used cars in major cities in India. Dataset used here is from a hackathon hosted by [MachineHack](https://www.machinehack.com/). Go to the hackathon [homepage](https://www.machinehack.com/course/predicting-the-costs-of-used-cars-hackathon-by-imarticus/) to know more about the dataset. The dataset set contains features like Location, Manufacture details, car features such as Fuel type, Engine, and usage parameters. Below is the app in working condition.

 <img class="ef so s t u dq ai ip" width="960" height="594" srcset="https://miro.medium.com/max/552/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 276w, https://miro.medium.com/max/1104/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 552w, https://miro.medium.com/max/1280/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 640w, https://miro.medium.com/max/1400/1*h5Zp7_iQM4CGRQI_fN-iwg.gif 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/864/1*h5Zp7_iQM4CGRQI_fN-iwg.gif">

<center><i>application predicts the price of used car</i></center>

### Files required:

If you are using your model make sure you have the following.
1. reqiurements.txt
- The text contains the dependencies necessary for the smooth running of your application.

2. application.py
- The main script which performs the real-time computation in the background.

3. index.html
- It is the webpage that acts as an interface between client/user and background process. index.html serves the collecting user-inputs, passes it along to application.py where predictions are computed, and renders the results on the client-side of the page.

I assume the app is working perfectly on your local. Let’s get started without further ado.

## Setting up Elastic Beanstalk Command Line Interface

Elastic Beanstalk is the AWS service to deploy, manage, and scale applications. To access the service we need to set-up AWS *Identity and Access Management* (IAM) which provides us admin access (we can add user and grant him certain permissions too) and followed by *Elastic Beanstalk CLI* which allow us to interact with the AWS from local. Let's proceed with IAM account creation.

Open the project directory in cmd or terminal. Going forward, all the commands have to be executed here.
### Create an IAM account
1. Login into AWS account (If don't have then, create one)

2. Search for IAM service and click

3. Select ```user``` in the dashboard on the left and click ```add user``` tab.

4. Type your *username* or for the user, you wish to add.

5. check **Programmatic access** and Leave AWS Management Console access unchecked as we want to use EB CLI from local instead of this, and click ```next: Permissions```.

6. Select ```Add user to group``` then click on ```create group```

7. Enter the Group name of your choice. All the users you created are added to this group. Enter **AWSElasticBeanstalkFullAccess** in the policy search box then select it and click on ```create group```. Now you have created a group and gave the users access to the AWSElasticBeanstalkFullAccess service. Click ```next: Tags```.

8. In the Add tags section, you can add key-value pairs, which is optional, to store user information such as employee e-mail, job role, etc. These tags help us organize, track, or control access for these users.

9. Review the user details and permissions then click on ``Create user``.

10. Download the ```.csv``` file which user access key and secret access key. Later you will need them to connect to **EB CLI**.

You have successfully IAM created your account. 

### Setting up EB CLI.

1. Make sure you have python installed (by default Linux distro includes python). You can confirm it by executing the following command in bash.
``` bash
    python --version
```

2. Also, make sure pip (Python package manager) is installed 
``` bash
    pip --version
```

3. Now that Python and pip have been verified, go ahead install EB CLI.
``` bash
    pip install awsebcli --upgrade --user
```
3. To setup **EB Cli** on your machine follow the steps described [here](https://github.com/aws/aws-elastic-beanstalk-cli-setup)

Finally, verify the EB CLI install, run.
``` bash
    eb --version
```

## Deployment on AWS 
Its time to deploy the app residing in local onto the cloud.
1. If you have only one profile in your account, you may initialize *awsebcli* using the following command.
``` bash
    eb init -i
```

**Note** : **In case of multiple profiles in your account.**
 
 A user may have more than two profiles in his account. One created *P1* (let say) for app deployment (Elastic Beanstalk) and another one *P2* for storage service (S3). When we use a simple ```eb init -i``` AWS does not know which user profile to select, it will proceed with default one, maybe, account created recently. In case it picks profile *P2*, the one created for accessing S3 service then it won't allow you to proceed further as you have not assigned permissions to use EB service to *P2*, only *P1* has it. To solve this issue you must add this profile in the AWS config file. Let's do that.
    
open config file ```~/.aws/config``` in your fav text editor. Add your profile name and credential details found in the ```credentials.csv``` file, downloaded while creating a profile.

``` bash
[profile 'profile name'] #enter profile name not group name
- aws_access_key_id = 'access key id'  
- aws_secret_access_key = 'access key'
```

You can add the credentials of multiple profiles here.

save and close.

initialize 'awsebcli' with the profile name.
``` bash
eb init --profile 'profile name'
```

make sure that the profile name in the config and the one you typed in the terminal must match.

**Note**: In case you are having issues, look for errors in the log file by typing 'eb logs'

2. select the region of your interest. You must choose the region based on where your client resides. In your serving Indian clients then it is appropriate to select a region in India or any other region close to it. You may go with the default region in your case.

3. Provide app name when prompted and then select default options for the rest of the queries.

### WSGIApplicationGroup setup

**Note**: If your app is simple, which only needs a light database for its functioning then you may skip this one. Or if it requires to load heavy libraries, which is true in my case, we have to customize the WSGI configuration file. WSGI (Web Server Gateway Interface) is an interface between client and project that facilitates interaction between them. Since in my sample project, I use python libraries such as pandas, sklearn, etc we need to tell the WSGI to enter Python sub-interpreter mode which turned off by default.

Before we create the web application, you need to customize the WSGI configuration file to inform it that you will be requiring the Python sub-interpreter mode.

* create a folder inside project root folder called ".ebextensions"
``` bash
    mkdir .ebextensions
```

* create a file in it called ```.ebextensions/wsgi_fix.config``` and add the following config settings into it
``` python
#add the following to wsgi_fix.config
files:
  "/etc/httpd/conf.d/wsgi_custom.conf":
    mode: "000644"
    owner: root
    group: root
    content: |
      WSGIApplicationGroup %{GLOBAL}
```

save and close.

Phew.. we have successfully set up a cloud environment. Its time to push our app onto the cloud.

Create a web application
```bash
eb create 'appname'
```
Take may take a while. you will get a successful message once it's done. By default, AWS expects your main ```.py``` script to be named as ```application.py```.

In case, you want to the keep different name you need to register it in the config file ```..elasticbeanstalk/$appname$.env.yml``` look for the line ```WSGIPath: application.py``` replace the default name (application.py) with yours.

To launch the application, type.

``` bash
eb open
```

Copy and paste the link in output printed in the browser to make sure the app is working as you desired. Congratulations!! you have successfully deployed your app on AWS.

**Warning**:

Wait..!!! don't go away, we are not done yet. AWS is counting every minute your app is running on EB since launch. we need to terminate it to avoid additional charges as most of the cloud services are not free.

Type below command

```bash
eb terminate 'environment name' #  same as the 'profile name'.
```

After a few seconds, you will receive a confirmation message. It is always a good idea to crosscheck by visiting the AWS dashboard and make sure there are no EC2 and Elastic Beanstalk accounts active. Use the following steps.

- Login to AWS console
- Enter for 'Elastic Beanstalk' in the search bar and select it.
- There should not be any instance running.
- repeat the same for 'EC2'

Now you may rejoice.