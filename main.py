from fastapi import FastAPI, UploadFile, Form ,Response, Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi_login.exceptions import InvalidCredentialsException
from typing import Annotated
import sqlite3

con = sqlite3.connect('db.db', check_same_thread=False)
cur = con.cursor()
# cur.execute(f"""
#             CREATE TABLE items (
#                 id INTEGER PRIMARY KEY,
#                 title TEXT NOT NULL,
#                 image BLOB,
#                 price INTEGER NOT NULL,
#                 description TEXT,
#                 place TEXT NOT NULL,
#                 insertAt INTEGER NOT NULL
#             );
#             """)
# cur.execute(f"""
# create table users(
# 	id text primary key,
# 	name	text not null,
# 	email	text not null,
# 	password text not null
# );
#             """)
app = FastAPI()


SECRET = "super-coding"
manager = LoginManager(SECRET,'/login') # access token 자동 생성 라이브러리


@manager.user_loader()
def query_users(data):
    print(f"Loading user with ID: {data}")  # 디버깅용 로그 추가
    WHERE_STATEMENTS = f'id="{data}"'
    if type(data) == dict:
        WHERE_STATEMENTS = f'''id="{data['id']}"'''
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    user = cur.execute(f"""
                       SELECT * FROM users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    print(f"User found: {user}")  # 사용자 정보 출력
    return user


@app.post('/login')
def login(id:Annotated[str,Form()], 
           password:Annotated[str,Form()]):
    user = query_users(id)
    if not user:
        raise InvalidCredentialsException # 에러메세지 던지기 , 401 자동생성
    elif password != user['password']:
        raise InvalidCredentialsException
    access_token = manager.create_access_token(data={
        'sub':{
            'id':user['id'],
            'name':user['name'],
            'email':user['email']
        }
    })
    return {'access_token':access_token}

@app.post('/items')
async def create_item(image:UploadFile, 
                title:Annotated[str,Form()], 
                price:Annotated[int,Form()], 
                description:Annotated[str,Form()], 
                place:Annotated[str,Form()],
                insertAt:Annotated[int,Form()],
                user=Depends(manager)):
    image_bytes = await image.read()
    cur.execute(f"""
                INSERT INTO items (title, image, price, description, place, insertAt)
                VALUES('{title}','{image_bytes.hex()}', {price}, '{description}', '{place}', {insertAt})
                """) # f""" """ 문자열 사이 변수넣을 때 쓰는 방법
    con.commit()
    return '200'



@app.get("/items")
async def get_items(user=Depends(manager)):
    print(f"Authenticated user: {user}")  # 디버깅용 로그 추가
    con.row_factory = sqlite3.Row # 컬럼명도 같이 가져옴(array 형식으로)
    cur = con.cursor() # connection의 현재 위치 cursor --> 업데이트 해줌
    rows = cur.execute(f"""
                       SELECT * from items
                       """).fetchall()
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))


@app.get('/images/{item_id}')
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0]
    return Response(content=bytes.fromhex(image_bytes), media_type='image/*')


@app.post('/signup')
async def signup(id:Annotated[str,Form()], 
                 password:Annotated[str,Form()],
                 name:Annotated[str,Form()],
                 email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES ('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    return '200'

app.mount("/", StaticFiles(directory="frontend", html=True),name="frontend")
