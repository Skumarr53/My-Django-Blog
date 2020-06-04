
## Building a model 
 
 In order to deploy a model we shold build one. the model ready to be deployed must be exported in ```.pkl``` file, a python object which the web development framework like flask expect. Since you are here to learn deployment I assume you have your ready for deployment, if not, you may use my sample app from this [repository](https://github.com/Skumarr53/Used-Car-Price-Prediction/tree/master/webApp). Download the files in a directory.

Open the project directory in cmd or terminal. All the commands has to be executed here.

## Setting up Elastic Beanstalk Command Line Interface

Elastic Beanstalk is the AWS service to deploy, manage and scale applications. In order to access the service we need to set-up AWS *Identity and Access Management* (IAM) which provide us admin access (we can add user and grant him  certain permissions too) and followed *Elastic Beanstalk CLI* which allow us to interact with the AWS from local. Let's proceed with creating IAM account.

### Create an IAM account
1. Login to AWS account (If don't have ,then, create one)

2. Search for IAM service and go

3. Select ```user``` in the dashboard on the left and click ```add user``` tab.

4. Type a your *username* or for the user you wish to add.

5. check **Programmatic access** and Leave AWS Management Console access unchecked as we want to use EB CLI from local instead of this, and click ```next: Permissions```.

6. Select ```Add user to group``` then click on ```create group```

7. Enter Group name of your choice. All the users you created are added to this group. Enter **AWSElasticBeanstalkFullAccess** in policy serach box then select it and click on ```create group```. Now you have created a group and gave the users access to AWSElasticBeanstalkFullAccess service. Click ```next: Tags```.

8. In the Add tags section you can add key value pairs, which is optional, to store user information such as employee e-mail, job role etc. These tags help us organize, track, or control access for these users.

9. review the user details and permissions then click on ``Create user``.

10. Download the .csv file with user access key and secret access key on your local. Later you will need this to connect to **EB CLI**.

You have successfully created your account.

### Setting up EB CLI.

1. Make sure you have python installed (by default Linux distro includes python). You can confirm it by exceuting following command in bash.
``` bash
    python --version
```

2. Also make sure pip (Python package manager) is installed 
``` bash
    pip --version
```

3. Now that Python and pip have been verified, go ahead install EB CLI.
``` bash
    pip install awsebcli --upgrade --user
```
3. To setup **ebcli** on your machine follow the steps decribed [here](https://github.com/aws/aws-elastic-beanstalk-cli-setup)

Finally, verfiy the EB CLI install, run.
``` bash
    eb --version
```

## Deployment on AWS 
Its time to deploy the app residing in local onto cloud.
1. initiate *awsebcli*
If you have only one profile in your account, you may use following command.
``` bash
    eb init -i
```

**Note** : **In case, you have multiple profiles in you account.**
 
 A user may have mnore than two profiles in his account. One created *P1* (let say) for app deployment (Elastic Beanstalk) and other one *P2* for storage service (S3). When we use a simple ```eb init -i``` aws does not know which user profile to select it will proceed with defualt one, may be, account created recently. In case it picks profile *P2* created for accessing S3 service then it won't allow you to proceed further as you have not assigned permissions to use EB service to *P2*, only *P1* has it. In order to solve this issue you must add this profile in aws config file. Lets do that.
    
open config file ```~/.aws/config``` in your fav text editor. Add your profile name and credential details found in the ```credentials.csv``` file, downloaded while creating profile.

``` bash
[profile 'profile name'] #enter profile name not group name
- aws_access_key_id = 'access key id'  
- aws_secret_access_key = 'access key'
```

You can add credentilas of multiple accounts here. 

save and close.

initialize 'awsebcli' with profile.
``` bash
eb init --profile 'profile name'
```

make sure that profile name in config and the one you typing in the terminal must match.

**Note**: In case you are having issues, look for errors in the log file by typing 'eb logs'

2. select the region of your interest. You must choose region based on where your client reside. In your servering indian clients then it is appropiate select a region in india or any other region close to it. You may go with default region in your case.

3. Provide app name when promted and then select default options for rest of the queries.

### WSGIApplicationGroup setup

**Note**: If your app is an simple which only needs light database for its fuctioning then you may skip this one. Or if it reqiures to load heavy libraires which is true, in my case, we have to customize WSGI configuration file. WSGI (Web Server Gateway Interface) is an interface between client and projcet that facilites interaction between them. Since in my sample project, I use python libraries such as pandas, sklearn etc we need to tell the WSGI to enter Python sub-interpretor mode which turned off by default.

Before we create the web application, you need to customize the WSGI configuration file to inform it that you will be requiring the Python sub-interpreter mode.

* create a folder under web application root folder called ".ebextensions"
``` bash
    mkdir .ebextensions
```

* create a file in it called "wsgi_fix.config"
``` bash
    vi .ebextensions/wsgi_fix.config
```

* add the following config into it
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

Phew.. we have successfully setup cloud environment. Its time to push our app onto cloud.

Create web application
``` bash
eb create 'appname'
```   

Take may take a while. you will get successful message once its done. 
By default, AWS expects your main ```.py``` script to be named as ```application.py```.

In case, you have differewnt name you need to regiter it in config file ```..elasticbeanstalk/$appname$.env.yml``` look for the line ```WSGIPath: application.py``` replace the default name (application.py) with yours.

To lauch application, type.
``` bash
eb open
```
Copy and paste the link in output printed in browser to make sure app is working as you desired. Congratulations!! you have succefully deployed your app on AWS.

Wait..!!! don't go away, we are not done yet. AWS is counting every minute your app is running on EB since launch. we need to terminate it to avoid additional charges as most of the cloud services are not free. 

Type below command 
``` bash
eb terminate 'enviorment name' #  the one you entered while initiating EB instance 'profile name'.
``` 

After sometime you will recieve confirmation message. It is always a good idea to crosscheck by visting AWS dashboard and make sure there are no EC2 and Elastic Beanstalk accounts active.
    - Login to AWS console
    - Enter for 'Elastic Beanstalk' in search bar and select it.
    - There should not be any instance running.
    - repeat the same for 'EC2' 

Now you may rejoice.


