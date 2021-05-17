from rest_framework.routers import DefaultRouter
# from quickstart import views
from file_reading.views import polygon

router = DefaultRouter(trailing_slash=False)

print("API file")

router.register('S100Verificationvalidation/102', polygon.S100V_V,basename='h5'),