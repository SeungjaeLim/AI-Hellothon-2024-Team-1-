from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, database

router = APIRouter()


@router.get("/", response_model=List[schemas.Elder])
def get_all_elders(db: Session = Depends(database.get_db)):
    """
    모든 노인 정보 제공
    """
    elders = crud.get_all_elders(db)
    if not elders:
        raise HTTPException(status_code=404, detail="No elders found")
    return elders


@router.get("/{elder_id}", response_model=schemas.Elder)
def get_elder_by_id(elder_id: int, db: Session = Depends(database.get_db)):
    """
    id로 특정 노인 정보 제공
    """
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")
    return elder


@router.post("/", response_model=schemas.Elder)
def create_elder(elder: schemas.ElderCreate, db: Session = Depends(database.get_db)):
    """
    새로운 노인 정보 생성
    """
    return crud.create_elder(db, elder)


@router.get("/{elder_id}/keywords", response_model=List[schemas.Keyword])
def get_elder_keywords(elder_id: int, db: Session = Depends(database.get_db)):
    """
    노인의 키워드 정보 제공 (현재 사용 X)
    """
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    keywords = crud.get_keywords_by_elder_id(db, elder_id=elder_id)
    if not keywords:
        raise HTTPException(status_code=404, detail="No keywords found for this elder")

    return keywords


@router.patch("/{elder_id}/keywords/{keyword_id}", response_model=schemas.KeywordPreference)
def toggle_keyword_preference(elder_id: int, keyword_id: int, db: Session = Depends(database.get_db)):
    """
    노인의 키워드 선호도 토글 (현재 사용 X)
    """
    elder = crud.get_elder_by_id(db, elder_id=elder_id)
    if not elder:
        raise HTTPException(status_code=404, detail="Elder not found")

    preference = crud.toggle_keyword_preference(db, elder_id=elder_id, keyword_id=keyword_id)
    if not preference:
        raise HTTPException(status_code=404, detail="Preference not found or could not be toggled")

    return preference
