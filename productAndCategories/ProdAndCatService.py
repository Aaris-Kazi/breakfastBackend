from .models import CategoriesModel, ProductModel
import logging

log = logging.getLogger(__name__)

class ProdAndCatService:

    def __init__(self):
        self.categories_model = CategoriesModel
        self.product_model = ProductModel



    def createCategory(self, data: dict):
        pass

    def updateCategory(self, name:str, data: dict):
        try:
            catModel = CategoriesModel.objects.get(name=name)
            catModel.is_active = data.get("is_active")
            catModel.save()
        except Exception as e:
            log.error(f"Exception occured during updating the category due to {e.args[0]}")
            
            raise e


    def getCategory(self):
        return self.categories_model.objects.all()


    def createProduct(self, data: dict):
        pass


    def getProduct(self):
        return self.product_model.objects.all()

    def getProductByCategory(self, category_name: str):
        return self.product_model.objects.filter(category__name=category_name)