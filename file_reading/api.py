from rest_framework.routers import DefaultRouter
from file_reading.views import S100READINGFILE
from file_reading.views import S100SAVEFILE
from file_reading.views import S100SIGNUPFILE
from file_reading.views import S100UPDATEFILE
from file_reading.views import S100FEATUREFILE
from file_reading.views import S100PORTRAILFILE
from file_reading.views import S100XMLFILE
from file_reading.views import S100Map
from file_reading.views import S100LOGFILE
from file_reading.views import S100ROLE
from file_reading.views import S100Agency
from file_reading.views import S100PASSWORD


router = DefaultRouter(trailing_slash=False)


router.register('S100Verification/Validation/file-reading/102', S100READINGFILE.S100FlieReadingViewset,basename='S100Verification'),
router.register('S100Verification/Validation/savecontent/102', S100SAVEFILE.S100SaveViewset,basename='save'),
router.register('S100Verification/Validation/signup', S100SIGNUPFILE.S100SignupViewset,basename='signup'),
router.register('S100Verification/Validation/filemodify', S100UPDATEFILE.S100ModifyViewset,basename='filemodify'),
router.register('S100Verification/Validation/Feature', S100FEATUREFILE.S100FeatureViewset,basename='feature'),
router.register('S100Verification/Validation/Portrail', S100PORTRAILFILE.S100PortrailViewset,basename='portrail'),
router.register('S100Verification/Validation/XML', S100XMLFILE.S100XMLViewset,basename='xml'),
router.register('S100Verification/Validation/S100map', S100Map.S100MapView,basename='map'),
router.register('S100Verification/Validation/Log', S100LOGFILE.S100LOGFILE,basename='log'),
router.register('S100Verification/Validation/Role', S100ROLE.S100RoleViewset,basename='role'),
router.register('S100Verification/Validation/Agency', S100Agency.S100AgencyViewset,basename='agency'),
router.register('S100Verification/Validation/changepassword', S100PASSWORD.S100PasswordViewset,basename='password'),

