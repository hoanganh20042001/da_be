# Import all the models, so that Base has them before being
# imported by Alembic
from app.models.model_base import Base  # noqa
from app.models.model_user import User  # noqa
from app.models.model_patients import Patients
from app.models.model_units import Units
from app.models.model_diseases import Diseases
from app.models.model_checks import Checks
from app.models.model_result import Results