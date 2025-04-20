from fastapi import APIRouter, Depends
from security import get_current_user

class ProtectedRouter(APIRouter):
    def __init__(self, *args, **kwargs):
        dependencies = kwargs.pop("dependencies", [])
        dependencies.append(Depends(get_current_user))
        super().__init__(*args, dependencies=dependencies, **kwargs)
