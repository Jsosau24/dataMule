"""
Jonathan Sosa 
helper_functions.py
may-jun 2023
"""

# functions on the file (you can look these up and it will take you there)
## create_user --> creates an user if it doesn't exist
##create_user_csv --> creates users using a CSV file
## get_file_extension --> returns the extension of a file

#imports
from werkzeug.security import generate_password_hash
from .models import Peak, Athlete, Coach, Admin, User
from werkzeug.utils import secure_filename
import pandas as pd
import os
from . import db

#functions
def create_user(colby_id, first_name, last_name, email, gender, class_year, type):
    """
    This functions creates new users
    ----------------------
    PARAMETERS:
    colby_id: int
    first_name: str
    last_name: str
    email: str
    gender: str
    class_year: int
    type:str
    ---------------------
    Return: if user is created returns an user
        else, (colby_id, error)
    """
    

    used_email = User.query.filter_by(email=email).first()

    if used_email == None:
        status = 0
        position = 'Other'
        password = generate_password_hash('Colby')

        try:
            if type == 'admin':
                new_user = Admin(
                    colby_id = colby_id,
                    first_name = first_name,
                    last_name =
                    last_name,
                    email = email,
                    password = password
                )
            
            elif type == 'peak':
                new_user = Peak(
                    colby_id = colby_id,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password
                )

            elif type == 'coach':
                new_user = Coach(
                    colby_id = colby_id,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password
                )
            
            elif type == 'athlete':
                new_user = Athlete(
                    colby_id = colby_id,
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    password = password,
                    gender = gender,
                    class_year = class_year,
                    status = status,
                    position = position
                )
            
            else:
                return False,[colby_id,'worng type of user']

            return True,new_user

        except:
            return False,[colby_id, "error on the try function"]
    
    else:
        return False,[colby_id, 'user exists']

def create_user_csv(file):
    """
    This functions creates new users
    ----------------------
    PARAMETERS:
    file: csv or excel file
    ---------------------
    Return: if user is created returns an user
        else, (colby_id, error)
    """
    
    filename = secure_filename(file.filename)
    try:
        extension = get_file_extension(filename)
        
        # get the df if it is a csv file
        if extension == '.csv':
            df = pd.read_csv(file)

        # get the df if it is an excel file
        elif extension == '.xlsx' or extension == '.xls':
            df = pd.read_excel(file)  

        # lowercases the columns to avoid error
        df.columns = df.columns.str.lower()

        # tries to create users, if not possible returns the error and colby id
        errors = []

        for index, row in df.iterrows():
            bol,user = create_user(
                colby_id = row['colby id'],
                first_name = row['name'],
                last_name = row['last name'],
                email = row['email'],
                gender = row['gender'],
                class_year = row['class year'],
                type = row['type']
            )
            # if the user was created
            if bol:
                db.session.add(user)
            # if the user wasnt created
            else:
                errors.append(user)

        db.session.commit()
        return errors
        

    except:
        return False,'error with the file'

def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()


