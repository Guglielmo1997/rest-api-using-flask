from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import jwt_required

from schemas import ShopSchemas
from models import ShopModel

blueprint = Blueprint("shop", __name__, description="Operation on Shop")

@blueprint.route("/shop/<shop_id>")
class Shop(MethodView):
    @jwt_required()
    @blueprint.response(200, ShopSchemas)
    def get(self, shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        return shop


    @jwt_required(fresh=True)
    def delete(self,shop_id):
        shop = ShopModel.query.get_or_404(shop_id)
        db.session.delete(shop)
        db.session.commit()
        return {'message': 'Shop Deleted'}


@blueprint.route("/shop")
class ShopList(MethodView):
    @jwt_required()
    @blueprint.response(202, ShopSchemas(many=True))
    def get(self):
        return ShopModel.query.all()

    @jwt_required(fresh=True)
    @blueprint.arguments(ShopSchemas)
    @blueprint.response(200, ShopSchemas)
    def post(self,shop_data):
        shop = ShopModel(**shop_data)
        try:
            db.session.add(shop)
            db.session.commit()
        except IntegrityError:
            abort(404, message='A shop with that name already Exist')
        except SQLAlchemyError:
            abort(500, message='Error occurred while inserting the shop')

        return shop
