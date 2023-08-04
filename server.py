

#imports

from urllib import request
from sklearn.feature_extraction.text import TfidfVectorizer
from pydantic import BaseModel
from fastapi import FastAPI, Request, Response,status, Form, HTTPException
from fastapi.responses import RedirectResponse
from pymongo import MongoClient
from bson import json_util
from bson.objectid import ObjectId
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Form, Cookie, Depends
#from starlette.responses import RedirectResponse, Response
import datetime,time
import jwt
import os
from passlib.context import CryptContext
import logging
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime
from fastapi import UploadFile
import shutil
import uvicorn

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder
import numpy as np
from newvalidate import recommend_financial_aid


client = MongoClient("mongodb://localhost:27017/")
# Database
StudentDB = client['StudentDB']
# Collection
stud = StudentDB['loginstudent']



#Model
class Students(BaseModel):
        stu_id: int
        stu_name: str
        stu_image: UploadFile  # Use UploadFile type for image uploads
        stu_password: str


#Initialize
app = FastAPI()





app.add_middleware(SessionMiddleware, secret_key="secret_key")

# Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#Static file serv
app.mount("/static", StaticFiles(directory="static"), name="static")
#Jinja2 Template directory
templates = Jinja2Templates(directory="templates")

app.add_middleware(SessionMiddleware, secret_key="secret_key")



@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/signin", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("signin.html", {"request": request})

@app.get("/guide", response_class=HTMLResponse)
def home(request: Request):
    student_id = request.session.get("student_id")
    signed_in = True if student_id else False

    student = None
    if signed_in:
        # Fetch the student details based on the 'student_id'
        student = stud.find_one({"stu_id": student_id})

    return templates.TemplateResponse(
        "guide.html",
        {"request": request, "signedIn": signed_in, "student": student}
    )


@app.post("/signin", response_class=HTMLResponse)
async def signin(request: Request, username: str = Form(...), password: str = Form(...)):
    user = stud.find_one({"stu_id": int(username)})
    if not user:
        message = "User not found"
        return templates.TemplateResponse("signin.html", {"request": request, "message": message})
    if user["stu_password"] != password:
        message = "Incorrect password"
        return templates.TemplateResponse("signin.html", {"request": request, "message": message})

    # Set the student ID in the session
    request.session["student_id"] = user["stu_id"]

    response = RedirectResponse(url='/dashboard1')
    return response

from pathlib import Path

@app.post("/signup")
async def signup(request: Request, stu_id: int = Form(...), stu_name: str = Form(...),
                 stu_image: UploadFile = Form(...), stu_password: str = Form(...),
                 confirm_password: str = Form(...)):
    # Perform validation checks
    if stu_password != confirm_password:
        message = "Passwords do not match"
        return templates.TemplateResponse("signup.html", {"request": request, "message": message})

    # Save the user data to the database or perform any other necessary actions
    new_student = {
        "stu_id": stu_id,
        "stu_name": stu_name,
        "stu_image": stu_image.filename,
        "stu_password": stu_password
    }
    stud.insert_one(new_student)

    # Save the uploaded image to a desired location within the static files directory
    image_path = Path("static/images") / stu_image.filename

    with open(image_path, "wb") as image_file:
        shutil.copyfileobj(stu_image.file, image_file)

    return templates.TemplateResponse("signin.html", {"request": request})


@app.post("/dashboard1", response_class=HTMLResponse)
async def dashboard_post(request: Request):
    # Retrieve the student ID from the session
    student_id = request.session.get("student_id")

    # Check if the student ID exists in the session
    if not student_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Find the student in the database
    student = stud.find_one({"stu_id": student_id})

    # Check if the student exists
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    result = stud.find({})
    return templates.TemplateResponse("dashboard1.html", {"request": request, "result": result, "student": student})

from typing import Optional

@app.get("/dashboard1", response_class=HTMLResponse)
async def dashboard_get(request: Request, student_id: Optional[str] = None):
    # Check if the student ID exists
    if student_id:
        # Find the student in the database
        student = stud.find_one({"stu_id": student_id})

        # Check if the student exists
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        return templates.TemplateResponse("dashboard1.html", {"request": request, "result": None, "student": student})

    # Retrieve the student ID from the session
    student_id = request.session.get("student_id")

    if student_id:
        # Find the student in the database
        student = stud.find_one({"stu_id": student_id})

        return templates.TemplateResponse("dashboard1.html", {"request": request, "result": None, "student": student})

    # Allow access to /dashboard1 without requiring sign-in
    return templates.TemplateResponse("dashboard1.html", {"request": request, "result": None, "student": None})





@app.get("/next", response_class=HTMLResponse)
def read_all_loginstudent(request: Request):
    result = stud.find({})
    print(result)
    return templates.TemplateResponse("list_fish.html", {"request": request, "signin": result})


# Other routes remain the same
dataset = pd.read_csv('D:/fastApiProject1/trainnew.csv', encoding='latin1', nrows=100)

# Split multi-valued columns
dataset['studylevel'] = dataset['studylevel'].apply(lambda x: [level.strip() for level in x.split(',')] if isinstance(x, str) else [x])
dataset['familyincome'] = dataset['familyincome'].apply(lambda x: [val.strip() for val in x.split(',')] if isinstance(x, str) else [x])
dataset['major'] = dataset['major'].apply(lambda x: [val.strip() for val in x.split('-')] if isinstance(x, str) else [x])

# Calculate similarity function
def cosine_similarity_score(set1, set2):
    vectorizer = TfidfVectorizer(use_idf=False)
    vectors = vectorizer.fit_transform([set1, set2])
    cosine_sim = cosine_similarity(vectors)[0][1]
    return cosine_sim * 100  # Convert to percentage

# Calculate similarity
def get_similarity(user_input, dataset_entry):
    similarity_scores = []
    for column_name in ['studylevel', 'familyincome', 'major', 'identity', 'state']:
        user_input_set = " ".join(user_input[column_name])
        dataset_entry_set = " ".join(dataset_entry[column_name])
        similarity = cosine_similarity_score(user_input_set, dataset_entry_set)
        similarity_scores.append(similarity)
    return np.mean(similarity_scores)  # Take the mean of individual cosine similarities

# Process form and get recommendation
@app.post("/result", response_class=HTMLResponse)
async def process_form(request: Request, study_level: str = Form(...), family_income: str = Form(...),
                      cgpa: float = Form(...), identity: str = Form(...), state: str = Form(...),
                      major_of_study: str = Form(...), subcategory: str = Form(...)):

    print("Received study_level:", study_level)
    print("Received family_income:", family_income)
    print("Received cgpa:", cgpa)
    print("Received identity:", identity)
    print("Received state:", state)
    print("Received major_of_study:", major_of_study)
    print("Received subcategory:", subcategory)

    # Check if any field is empty
    if not all([study_level, family_income, subcategory, cgpa, identity, state]):
        error_message = "Please fill in all the required fields."
        return templates.TemplateResponse("dashboard1.html", {"request": request, "error_message": error_message})

    # Convert user input to lowercase for case insensitivity
    study_level = study_level.lower()
    family_income = family_income.lower()
    identity = identity.lower()
    state = state.lower()
    user_subcategory = subcategory.lower()

    # Filter financial aid options based on user criteria
    filtered_aid = dataset[
        (dataset['studylevel'].apply(lambda x: isinstance(x, list) and study_level in [level.lower() for level in x])) &
        (dataset['familyincome'].apply(lambda x: any(family_income in val.lower() for val in x))) &
        (dataset['major'].apply(lambda x: any(user_subcategory.lower() in val.lower() for val in x))) &
        (dataset['identity'].apply(lambda x: identity in x.lower())) &
        (dataset['state'].apply(lambda x: state in x.lower())) &
        (dataset['cgpa'].apply(lambda x: len(x.split(',')) == 2))  # Check for valid CGPA format
    ]

    filtered_aid = filtered_aid[
        (filtered_aid['cgpa'].apply(lambda x: float(x.split(',')[0].replace(',', '.'))) <= cgpa) &
        (filtered_aid['cgpa'].apply(lambda x: float(x.split(',')[1].replace(',', '.'))) >= cgpa)
    ]

    # Calculate similarities for all filtered financial aid options
    def calculate_similarities(user_input):
        similarities = [get_similarity(user_input, dataset_entry) for _, dataset_entry in filtered_aid.iterrows()]
        return similarities

    # Convert user input to a DataFrame
    user_input = pd.DataFrame({
        'studylevel': [study_level],
        'familyincome': [family_income],
        'cgpa': [cgpa],
        'major': [user_subcategory],  # You can replace this with your subcategory input if needed
        'identity': [identity],
        'state': [state]
    })

    # Calculate similarities for user input and filtered financial aid options
    filtered_aid['similarity'] = calculate_similarities(user_input)

    # Step 8: Sort financial aid options by similarity in descending order
    filtered_aid_sorted = filtered_aid.sort_values(by='similarity', ascending=False)

    # Format similarity scores with two decimal places and handle NaN values
    filtered_aid_sorted['similarity'] = filtered_aid_sorted['similarity'].apply(
        lambda x: '{:.2f}'.format(x) if not np.isnan(x) else 'N/A')

    # Print the filtered and sorted financial aid options with similarity scores
    print("Filtered Aid:")
    print(filtered_aid_sorted[['finaidname', 'similarity']])

    return templates.TemplateResponse("result.html", {"request": request,
                                                      "recommendations": filtered_aid_sorted.to_dict(orient='records')})


from typing import Optional


from fastapi.responses import JSONResponse  # Add this line
from fastapi import Request, Form, HTTPException
from datetime import datetime

# Endpoint to check if the user is signed in
@app.get("/check-signed-in")
async def check_signed_in(request: Request):
    student_id = request.session.get("student_id")
    signed_in = True if student_id else False

    student = None
    if signed_in:
        # Fetch the student details based on the 'student_id'
        student = stud.find_one({"stu_id": student_id})

    return JSONResponse({"signedIn": signed_in})



# Endpoint to save recommendation



@app.post("/save-recommendation")
async def save_recommendation(request: Request):
    # Retrieve the student ID from the session
    student_id = request.session.get("student_id")

    # Check if the student ID exists in the session
    if not student_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Find the student in the database
    student = stud.find_one({"stu_id": student_id})

    # Create the recommendations field if it doesn't exist
    if "recommendations" not in student:
        stud.update_one({"stu_id": student_id}, {"$set": {"recommendations": []}})

    # Get the recommendation data from the request body
    recommendation_data = await request.json()
    recommendation_name = recommendation_data.get("recommendation_name")
    recommendation_link = recommendation_data.get("recommendation_link")

    # Add the recommendation to the recommendations list
    current_datetime = datetime.now()
    recommendation = {
        "finaid_name": recommendation_name,
        "finaid_link": recommendation_link,
        "date": current_datetime.strftime("%Y-%m-%d"),
        "time": current_datetime.strftime("%I:%M %p")
    }
    stud.update_one({"stu_id": student_id}, {"$push": {"recommendations": recommendation}})

    # Return a response indicating success
    return {"message": "Recommendation saved successfully"}

@app.get("/shortlist", response_class=HTMLResponse)
async def shortlist(request: Request):
    # Retrieve the student ID from the session
    student_id = request.session.get("student_id")

    # Check if the student ID exists in the session
    if not student_id:
        message = "Please sign in first"
        return templates.TemplateResponse("shortlist.html", {"request": request, "message": message, "student": None})

    # Find the student in the database
    student = stud.find_one({"stu_id": student_id})

    # Get the saved recommendations
    recommendations = student.get("recommendations", [])

    context = {
        "request": request,
        "student": student,
        "recommendations": recommendations
    }

    return templates.TemplateResponse("shortlist.html", context)



@app.delete("/delete-recommendation/{recommendation_index}")
async def delete_recommendation(recommendation_index: int, request: Request):
    # Retrieve the student ID from the session
    student_id = request.session.get("student_id")

    # Check if the student ID exists in the session
    if not student_id:
        raise HTTPException(status_code=401, detail="Unauthorized")

    # Find the student in the database
    student = stud.find_one({"stu_id": student_id})

    # Check if the student exists
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    # Get the recommendations array
    recommendations = student.get("recommendations", [])

    # Check if the recommendation index is valid
    if recommendation_index < 0 or recommendation_index >= len(recommendations):
        raise HTTPException(status_code=404, detail="Recommendation not found")

    # Remove the recommendation at the specified index
    deleted_recommendation = recommendations.pop(recommendation_index)

    # Update the student's recommendations in the database
    stud.update_one({"stu_id": student_id}, {"$set": {"recommendations": recommendations}})

    # Return the deleted recommendation
    return {"message": "Recommendation deleted successfully", "deleted_recommendation": deleted_recommendation}


from fastapi import Request, HTTPException, Form
from starlette.responses import RedirectResponse

# Logout endpoint
@app.get("/logout")
def logout(request: Request):
    # Clear the session data or destroy the session
    request.session.clear()

    # Redirect to the index.html template or any other desired page
    return RedirectResponse(url='/')

@app.post("/save-rating")
def save_rating(rating: int):
    # Save the rating to the database
    save_rating_to_database(rating)

    # Return a response indicating the rating was saved successfully
    return {"message": "Rating saved successfully"}


# Function to save the rating to the database
def save_rating_to_database(rating):
    # Implement your database saving logic here
    # Connect to the database, create a new document in the collection,
    # and save the rating value

    import pymongo

    # Function to save the rating to the database
    def save_rating_to_database(rating):
        # Connect to MongoDB
        client = pymongo.MongoClient("mongodb://localhost:27017/")

        # Get the database
        db = client["your_database_name"]

        # Create the collection if it doesn't exist
        if "your_collection_name" not in db.list_collection_names():
            db.create_collection("your_collection_name")

        # Get the collection
        collection = db["your_collection_name"]

        # Insert the rating data into the collection
        rating_data = {"rating": rating}
        collection.insert_one(rating_data)

