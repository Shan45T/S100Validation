from rest_framework.routers import DefaultRouter
from validation.views import S100VALIDATION
from validation.views import S100PRODUCTLINE
from validation.views import role
from validation.views import S100AGENCY

router_validation = DefaultRouter(trailing_slash=False)
router_validation.register('S100Verification/Validation/file-validation/102', S100VALIDATION.S100FileValidationViewset,basename='S100Verification'),
router_validation.register('S100Verification/Validation/productline', S100PRODUCTLINE.S100ProductlineViewset,basename='product'),
router_validation.register('S100Verification/Validation/role', role.S100RoleViewset,basename='role'),
router_validation.register('S100Verification/Validation/agency', S100AGENCY.S100AgencyViewset,basename='agency'),

