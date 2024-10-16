from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from config.database import get_db
from auth.auth_bearer import get_user_id_from_token
from models.models import Users, SystemRoles, Modules, RoleModuleRelation

def get_current_user(request: Request, db: Session = Depends(get_db)):
    token = request.headers.get("Authorization")
    if not token:
        raise HTTPException(status_code=400, detail="Token no proporcionado")
    
    token = token.split(" ")[1]
    user_id = get_user_id_from_token(token)

    if not user_id:
        raise HTTPException(status_code=400, detail="Usuario no autenticado")

    user = db.query(Users).filter(Users.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return user_id

def check_permissions_factory(module_name: str):
    def check_permissions(request: Request, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
        user_role = db.query(Users.role_id).filter(Users.id == user_id).first()[0]
        module_id = db.query(Modules.id).filter(Modules.name == module_name).first()[0]
        permissions = db.query(RoleModuleRelation.create.label("escritura"), RoleModuleRelation.read.label("lectura"), RoleModuleRelation.update.label(("modificacion")), RoleModuleRelation.delete.label("eliminacion")).filter(
            RoleModuleRelation.role_id == user_role,
            RoleModuleRelation.module_id == module_id
        ).first()

        # Verificar permisos según el método HTTP y el nombre del módulo
        if request.method == "POST" and not permissions[0]:
            raise HTTPException(status_code=403, detail=f"No tiene permisos de escritura en el módulo {module_name}")
        if request.method == "GET" and not permissions[1]:
            raise HTTPException(status_code=403, detail=f"No tiene permisos de lectura en el módulo {module_name}")
        if request.method == "PUT" and not permissions[2]:
            raise HTTPException(status_code=403, detail=f"No tiene permisos de modificación en el módulo {module_name}")
        if request.method == "DELETE" and not permissions[3]:
            raise HTTPException(status_code=403, detail=f"No tiene permisos de eliminación en el módulo {module_name}")

        return user_id

    return check_permissions