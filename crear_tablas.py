from db.database import engine , Base
from models import *

Base.Metadata.create_all(bind=engine)
print("tablas creadas correctamente")