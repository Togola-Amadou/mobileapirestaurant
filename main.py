from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from database import SessionLocal, engine
from model import Panier, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)
app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tu peux mettre ton domaine ou "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class PanierCreate(BaseModel):
    name: str
    description: str
    image: str
    price: int


class PanierOut(PanierCreate):
    id: int

    class Config:
        orm_mode = True


@app.post("/paniers/", response_model=PanierOut)
def create_panier(panier: PanierCreate, db: Session = Depends(get_db)):
    db_panier = Panier(**panier.dict())
    db.add(db_panier)
    db.commit()
    db.refresh(db_panier)
    return db_panier

@app.get("/paniers/{panier_id}", response_model=PanierOut)
def read_panier(panier_id: int, db: Session = Depends(get_db)):
    db_panier = db.query(Panier).filter(Panier.id == panier_id).first()
    if db_panier is None:
        raise HTTPException(status_code=404, detail="Panier not found")
    return db_panier

@app.get("/paniers/", response_model=list[PanierOut])
def read_paniers(db: Session = Depends(get_db)):
    paniers = db.query(Panier).all()
    return paniers


@app.delete("/paniers/{panier_id}", response_model=PanierOut)
def delete_panier(panier_id: int, db: Session = Depends(get_db)):
    db_panier = db.query(Panier).filter(Panier.id == panier_id).first()
    if db_panier is None:
        raise HTTPException(status_code=404, detail="Panier not found")
    db.delete(db_panier)
    db.commit()
    return db_panier

