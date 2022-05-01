import imp
from fastapi import APIRouter
from resources.userController import router as userRouter
from resources.authController import router as authRouter
from resources.addressController import router as addRouter



router = APIRouter()

router.include_router(userRouter, tags=['user'])
router.include_router(authRouter, tags=['auth'])
router.include_router(addRouter, tags=['address'])

