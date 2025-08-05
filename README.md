# Popmart Web Scraping Script

Ensure that all libraries needed are installed within your system. Including Selenium, BeautifulSoup4, and Googlesheets API.

First, you must setup and create a google cloud project. No links will be provided. Pictures will be provided as necessary.

Next a service account for the project must be created with owner access. Navigate to **IAM & Admin** and on the leftmost section navigate to **Service Accounts**.

Once created, you will need to create a key. This will be stored in a credentials file within this project that you must make. To do so, stay on the **Service Accounts** section, click on the newly created account, and navigate to **Keys**. Then press Add key and create new existing key. Make sure you press JSON format and store this in your system as you will not be able to get this json file from the back.

Create a google sheet and obtain the ID for the sheets.

Input fields as necessary within the main.py file. Add the email of your service account into the google sheets you are using.

You may Change as needed :smile:

## Setup Example for Google Cloud Projects
### Creating a project
![Select a Project/Create](images/SelectProj.png)
![Create a new Project](images/NewProj.png)

### Create a Service Account for the project
![IAMAdmin navigation after creation](images/IAMAdmin.png)
![Service account navigation](images/ServAcc.png)
![Creation](images/Create.png)

### Create a key for the service account
![Keys Navigation](images/Keys.png)
![Add new Key](images/Add.png)
![JSON format](images/json.png)

## Example Google Sheet
![Sheets](images/GoogleSheets.png)