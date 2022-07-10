from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app= FastAPI()

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Post(BaseModel):
    customer_name: str
    email: str
    mobile_number: str
    city: str

class porder(BaseModel):
    product_name: str
    quantity: int
    pricing: int
    mrp: int
    
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='Intugine_api' , user='postgres', password='8790', cursor_factory=RealDictCursor)
        cursor=conn.cursor()
        print("Database connection was succesfull!")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error:",error)
        time.sleep(2)

my_posts = [{"title": "title of post 1","content":"content of post 1", "id":1},{"title":"favourite foods","content":"I like pizza","id":2}]

def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.get("/")
def read_root():
    return {"Message": "Welcome to my api!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM products""")
    posts = cursor.fetchall()
    return {"data":posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO products(customer_name, email, mobile_number, city) VALUES(%s, %s ,%s, %s) RETURNING *""",(post.customer_name, post.email, post.mobile_number, post.city))

    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}
# title str, content str


@app.get("/posts/{id}")
def get_post(id: int):
    post = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    print(post)
    return{"post_detail":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index= find_index_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int,post: Post):
    index= find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {'data': post_dict}



@app.get("/purchaseorder", status_code=status.HTTP_201_CREATED)
def purchaseorder():
    cursor.execute("""SELECT * FROM purchase_order""")

    new_post = cursor.fetchall()
    conn.commit()
    return {"data": new_post}

