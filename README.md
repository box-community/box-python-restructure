<img src="images/box-dev-logo.png" 
alt= “box-dev-logo” 
style="margin-left:-10px;"
width=40%;>


# Box Python Folder Restructure
This sample code will help you jumpstart restructuring a Box folder tree using Python. It goes alongside a [blog post](https://medium.com/box-developer-blog/restructuring-the-box-folder-tree-with-python-31aeb7e051da). Make sure to check that out for more details. It does not add or alter collaborations. 

It is highly recommended to test and develop in a Sandbox or non-production environment. It also recommended to the run the script as a user that owns the content. The demo uses an OAuth free user account, but in an enterprise instance with collaborators, results may vary. 


## Box configuration steps
If you want to start from scratch, follow all steps. If you'd like to use a currently existing Box instance, like a sandbox - skip to step 3.

1. Create a [Box free account](https://www.box.com/pricing/individual) if you don't already have one.
2. Complete the registration process by verifying your email and login to Box.
3. Navigate to the [Box Developer Console](https://app.box.com/developers/console). This will activate a developer account. Note - With a free account, you can only create OAuth 2.0 applications. You also won't have access to the admin console. For the purposes of this demo, it is not needed; however, in a real world environment, you would want access to the features available to an admin in Box. For example, creating groups, users, or logging in as another user.
4. Create a new Box application. Select Custom App, fill in the form and then click Next.
5. Select User Authentication (OAuth 2.0) and then click Create App.
6. Scroll down to Redirect URIs and add the following redirect URI:
    - http://127.0.0.1:5000/callback
    - (or whatever you have configured in the .env file)
7. Check all boxes in application scopes.
    - (or only what you think will be necessary)
8. Click Save Changes.
9. Note the Client ID and Client Secret. You will need these later.

## Installation and configuration

You will need to have [python](https://www.python.org/downloads/) installed on your machine. We show using [Visual Studio Code](https://code.visualstudio.com/), but you can use the code editor of your choice.

> Get the code
```bash
git clone git@github.com:box-community/box-python-restructure.git
cd box-python-restructure
```

> Set up your virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

> Create your local application environment file
```bash
cp .env.sample .env
```

> Open the code in the code editor of your choice.
```
code .
```

> Update the CLIENT_ID and CLIENT_SECRET field values in the env file with the Box application client id and client secret you created on the developer console.

## Running the application 
The included code will restructure a folder tree as described in the [blog post](https://medium.com/box-developer-blog/restructuring-the-box-folder-tree-with-python-31aeb7e051da).

You are free to make changes to the main.py file if you wish to change the underlying logic. Just remember, migrating folders with large amounts of data can and will trigger [LFOs](https://support.box.com/hc/en-us/articles/360055677914-Large-File-Operation-Warnings-in-Admin-Console-). You will want to build in error and/or timing logic for any migrations that could cause those.

Collaboration changes are not part of this script.

The first time you run the application, it should open a web browser window and prompt you to log in to Box. 
After you log in, it will ask you to authorize the application.
Once this process is complete you can close the browser window.

The authorization token lasts for 60 minutes, and the refresh token for 60 days.
If you get stuck, you can delete the .outh.json file and reauthorize the application.
If you don't use the application for over 60 days, you will need to reauthorize the application.

### Create demo folder tree
In order to run the demo code, you will want to setup a folder tree that can be reorganized. There is a demo pdf file and a demo.py file for you to use to setup a demo tree. Note - it doesn't set up any collaborations. To run the demo piece, use the below command.

It will automatically delete a Human Resources folder if it already exists. It also automatically replaces the human resources parent folder id in the .env file for use in the next step. By default it creates 10 employees with five files in each subfolder. You are welcome to change these numbers in the code.

```bash
python3 demo.py
```

### Run the script
The included script by default restructures content based on the example included in the blog post. You are free to change the logic or variables in the script. To run the script, use the below command.

```bash
python3 main.py
```

If you want to use different folder naming conventions, you can change the variables at the bottom of the main.py file. If you use the demo.py file to create the structure, you will need to change that file too.

```
    parent_folder_id = os.getenv("PARENT_FOLDER_ID")
    folder_name = 'Employees'
    subfolder_names = ['Personnel', 'Confidential']
```

### Questions
If you get stuck or have questions, make sure to ask on our [Box Developer Forum](https://forum.box.com)