from flask import Flask
from flask_sqlalchemy import SQLAlchemy, Model
from importlib import import_module
from pathlib import Path
from typing import List, Type, Any

db = SQLAlchemy()

APP_MODULE = Path(__file__).resolve().parent.parent.name

def get_modules(module: str) -> List[str]:
    module_dir = Path(__file__).resolve().parent.parent / module
    return [
        str(p.relative_to(module_dir)).replace('/', '.').removesuffix('.py')
        for p in module_dir.glob('**/*.py')
        if p.name != '__init__.py'
    ]

def dynamic_loader(module: str, compare: callable) -> List[Type[Model]]:
    items = []
    for mod in get_modules(module):
        module = import_module(f'{APP_MODULE}.{module}.{mod}')
        if hasattr(module, '__all__'):
            objs = [getattr(module, obj) for obj in module.__all__]
            items += [obj for obj in objs if compare(obj) and obj not in items]
    return items

def is_model(item: Any) -> bool:
    return (
        isinstance(item, type) and issubclass(item, Model)
        and not getattr(item, '__ignore__', False)
    )

def init_db(app: Flask, db: SQLAlchemy) -> None:
    with app.app_context():
        for model in dynamic_loader('models', is_model):
            setattr(__name__, model.__name__, model)
        db.init_app(app)