from decimal import Decimal
from tokenize import Double
from unicodedata import decimal
from fastapi import Depends, APIRouter, HTTPException, Request, status
from sqlalchemy.orm import Session
from sqlalchemy import or_
from models.schemas import schemas
from models import  models, get_db
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from resources.utils import distance_calculator



router = APIRouter()


@router.post('/address-create/', summary="Create Address with coordinates")
def address_create(address: schemas.Address ,db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.latitude == address.latitude, models.Address.longitude == address.longtitude, models.Address.is_deleted == False).first()
    if db_address:
        raise HTTPException(status_code=400, detail="Address already exist")
    db_address = models.Address(
    name=address.name.lower(), 
    address_label=address.address_label.lower(),
    address=address.address.lower(), 
    phone_no=address.phone_no,
    pincode=address.pincode, 
    latitude=address.latitude, 
    longitude=address.longtitude
    )
    db.add(db_address)
    db.commit()
    db.refresh(db_address)
    return HTTPException(status_code=200, detail=db_address)

@router.get('/address/all', summary='Retrieves all the address from the database')
def get_all_address(db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.is_deleted == False).all()
    return HTTPException(status_code=200, detail=db_address)

@router.patch('/address/{address_uuid}', summary='Retrieves a particular address with the given Address UUID')
def update_address(address_uuid: str ,address: schemas.Address ,db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.uuid == address_uuid, models.Address.is_deleted == False).first()
    if db_address:
        db_address.name = address.name
        db_address.address_label = address.address_label
        db_address.address = address.address
        db_address.phone_no = address.phone_no
        db_address.pincode = address.pincode
        db_address.latitude = address.latitude
        db_address.longitude = address.longtitude
        db.commit()
        db.refresh(db_address)
        return HTTPException(status_code = 200, detail = "Address Updated successfully")
    else:
        return HTTPException(status_code = 400, detail = "Address not found")

@router.delete('/address/{address_uuid}', summary='Deletes address with the given Address UUID')
def delete_address(address_uuid: str ,db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.uuid == address_uuid, models.Address.is_deleted == False).first()
    if db_address:
        db_address.is_deleted = True
        db.commit()
        db.refresh(db_address)
        return {'message' : 'Address deleted successfully'}
    else:
        return {'message' : 'Address Not Found'}


@router.post('/address/distance-calculator/', summary="Gets all the addresses from the given distance and coordinates")
def distance_cal(cordinates: schemas.Cordinates, db: Session = Depends(get_db)):
    db_address = db.query(models.Address).filter(models.Address.is_deleted == False).all()
    data = []
    for r in db_address:
        lat2 = r.latitude
        long2 = r.longitude
        l1 = Decimal(lat2)
        l2 = Decimal(long2)
        calculated_distance = distance_calculator(cordinates.latitude, cordinates.longtitude, l1, l2)
        if calculated_distance <= cordinates.distance:
            location = db.query(models.Address).filter(models.Address.uuid == r.uuid).first()
            distance = {
                'location' : location,
                'distance' : '{} KM'.format(calculated_distance),
                }
            data.append(distance)
    return HTTPException(status_code=200, detail=data)

@router.post('/address/cal-distance-btw-two-cordinates/', summary='Calculates the distance two coordinates')
def cal_two_cordinates(cordinates: schemas.Cal_two_cordinates, db: Session = Depends(get_db)):
    try:
        calculated_distance = distance_calculator(cordinates.latitude1, cordinates.longtitude1, cordinates.latitude2, cordinates.longtitude2)
        data = {
            'distance' : calculated_distance
        }
        return HTTPException(status_code=200, detail=data)
    except:
        return HTTPException(status_code=400, detail="Please Enter valid cordinates")
