## Image-Processing With Tesseract-OCR
- Push the pdf file to Convert the text from image to text (using     
  Tesseract-OCR).
- Build a webapp with Flask
- Deploy the Model With Flask on Heroku.

### Software And Tools Requirements
1. [Github Account](https://github.com)
2. [VSCODEIDE](https://code.visualstudio.com/)
3. [HerokuAccount](https://heroku.com)
4. [GitCLI](https://git-scm.com/book/en/v2/Getting-Started-The-Command-Line)


### Create a new enviroment:
- conda create -p python==3.7 -y

### Buid a webapp with Flask:
   - pip install -r requirements.txt
   - To import numpy, pandas etc... Need to activate (venv) of Flask. 
     then: pip install -r requirments-- which will import all the necessary libraries updated in requirments.txt
   - Refer to "requirements.txt" for details of dependencies
   - Creat "app.py" for API.
   - Run python app.py in cmd terminal to excute the API.

### Upload to Github:
   - Used GIT CLI: for cloning: git config --global user.name and git config --global user.email and to commit and 
     push.

### Procfile: 
   - To deploy in heroku, it specifies some commands that needs 
     to be executed by the app as soon as it starts. It is basically indicating what is giving a kind of command to the heroku instance itself.
   - web: gunicorn app:app --green unicorn - purest python   
     https server to run python application by calling app.py in procfile.

## 3. Deploy the App on Heroku
   - Prepare: Procfile, requirements.txt.
   - Login into Heroku accout.
   - Create a new app
   - Choose Github(Connect to Github) 
   - Validate your github account to connect with heroku.
   - Search and connect for the repo that you want to connect.
   - Choose auto deploy/manual as per the requirement.
   - Choose branch and click on deploy.



## Docker
  - With the help of this file whatever information i am  
    actually writing, it created a docker image and that docker image can be taken and it can be run within a container which we specifically say it can be run as docker container in any OS based on base configuration in docker hub which can be used in any system for deploymemt.
  - Create docker image using command like: from, copy, 
    workdir, run, expose and CMD.
  - Configure github actions- 2 folders need to be created:
    .github\workflows
  - Inside .github\workflows main.yaml needs to be created  
    which will define the entire workflow.
  - Push the docker image in the form of container to the 
    heroku platform so the entire configuration over here will be set up in this main.yaml.
  - To make this as CI/CD pipeline we need to take some secret 
    keys from heroku and main.yaml and add that in github actions. This key will indicate which account i am using in heroku.
  - Build, Push and Release a docker container to heroku will 
    happen automatically from the github repository itself.
  - git add: To add the all the files in github repo.
  - git commit and push.
  - Click on details tab in github to run the jobs & 
    automatically deployment happens in github.
  - Once the job is completed in github, open the app in heroku.

  ### Note:
- To enhance the date quality of images we could use  
  hugging face or use CTPN for localisation and CRNN for OCR but for that we must have good system configuration with GPU.