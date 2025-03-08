from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import select
import base64
from db import User, Ads, Config


app=FastAPI()
Config.migrate()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/token") 
async def token (form: OAuth2PasswordRequestForm = Depends()): 
    with Config.SESSION as session: 
        user = session.exec(select(User).where(User.username == form.username)).first()
        if user.password==form.password:
            return {"access token": form.username, "token, type": "bearer"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Dont have such user")


@app.post("register")
async def register(user:User):
    sample_string = user.password
    in_bytes = sample_string.encode("ascii")
    base64_bytes = base64.b64encode(in_bytes)
    base64_string = base64_bytes.decode("ascii")
    user.password == base64_string

    with Config.SESSION as session:
        data = user
        session.add(data)
        session.commit()
        session.refresh(data)
        return user


@app.get("/users/")
async def users(token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        return session.exec(select(User)).all()


@app.post("/ads/")
async def add_ads(data: Ads, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        session.add(data)
        session.commit()
        session.refresh(data)
        return data
    

@app.get("/read-ads/")
async def read_ads():
    with Config.SESSION as session:
        return session.exec(select(Ads)).all()
    

@app.delete("buy-ads")
async def delete_ads(ads_id:int, token = Depends(oauth2_scheme)):
    with Config.SESSION as session:
        data = session.get(Ads, ads_id)
        if not data:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="We dont have this ads")
        session.delete(data)
        session.commit()
        return "You successfully buy this ads"


"""
5. Розробка ендпоінтів для отримання списку оголошень з бази даних.

Створіть систему чату, яка дозволить покупцям та продавцям в реальному часі обмінюватися повідомленнями. Використайте технологію WebSocket, яка інтегрується в FastAPI, для створення постійного з'єднання між сервером та клієнтами.
На фронтенді створіть користувацький інтерфейс для чату. Це може включати вікно чату, де користувачі можуть бачити історію повідомлень та вводити нові повідомлення.
На бекенді реалізуйте логіку для прийому та відправлення повідомлень через WebSocket. Це включає в себе відкриття з'єднань, обробку вхідних повідомлень від користувачів та відправлення відповідей.
Забезпечте, щоб лише автентифіковані користувачі могли використовувати чат. Використайте систему автентифікації OAuth2 для перевірки користувачів, які намагаються встановити з'єднання WebSocket.
"""