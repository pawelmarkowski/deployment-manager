import grpc
from google.protobuf import empty_pb2
from sqlalchemy.orm import joinedload, subqueryload

class GenericServicer:
    def __init__(self, model, converter, db_session_factory):
        self.model = model
        self.converter = converter
        self.db_session_factory = db_session_factory
        self.load_options = self._get_load_options()

    def _get_db(self):
        return self.db_session_factory()

    def _get_load_options(self):
        # This can be overridden by subclasses if needed
        return []

    def Create(self, request, context):
        db = self._get_db()
        try:
            # Simple conversion from request to model fields
            model_args = {field.name: getattr(request, field.name) for field in request.DESCRIPTOR.fields}
            db_item = self.model(**model_args)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            # Refresh parent relationships if they exist
            for rel in self.model.__mapper__.relationships:
                if hasattr(db_item, rel.key):
                    parent = getattr(db_item, rel.key)
                    if parent:
                        db.refresh(parent)
            return self.converter(db_item)
        finally:
            db.close()

    def Get(self, request, context):
        db = self._get_db()
        try:
            db_item = db.query(self.model).options(*self.load_options).filter(self.model.id == request.id).first()
            if db_item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'{self.model.__name__} not found')
                return self.model()
            return self.converter(db_item)
        finally:
            db.close()

    def List(self, request, context):
        db = self._get_db()
        try:
            db_items = db.query(self.model).options(*self.load_options).all()
            return [self.converter(item) for item in db_items]
        finally:
            db.close()

    def Delete(self, request, context):
        db = self._get_db()
        try:
            db_item = db.query(self.model).filter(self.model.id == request.id).first()
            if db_item is None:
                context.set_code(grpc.StatusCode.NOT_FOUND)
                context.set_details(f'{self.model.__name__} not found')
                return empty_pb2.Empty()
            db.delete(db_item)
            db.commit()
            return empty_pb2.Empty()
        finally:
            db.close()