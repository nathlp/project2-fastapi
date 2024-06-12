from fastapi.testclient import TestClient
from fastapi import status
from app.db.models import Product as ProductModel
from app.main import app


client = TestClient(app)

def test_add_product_route(db_session, categories_on_db):
    body = {
        "category_slug": categories_on_db[0].slug,
        "product":{
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 22.99,
            "stock": 22
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_201_CREATED

    product_on_db = db_session.query(ProductModel).all()
    
    assert len(product_on_db) == 1

    db_session.delete(product_on_db[0])
    db_session.commit()


def test_add_product_route_invalid_slug(db_session):
    body = {
        "category_slug": "invalid",
        "product":{
            "name": "Camisa Mike",
            "slug": "camisa-mike",
            "price": 22.99,
            "stock": 22
        }
    }

    response = client.post('/product/add', json=body)

    assert response.status_code == status.HTTP_404_NOT_FOUND

    product_on_db = db_session.query(ProductModel).all()
   
    assert len(product_on_db) == 0

   
