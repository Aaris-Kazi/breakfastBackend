from .models import CategoriesModel, ProductModel

class ProdAndCatService:

    def __init__(self):
        self.categories_model = CategoriesModel
        self.product_model = ProductModel



    def createCategory(self, data: dict):
        pass


    def getCategory(self):
        return self.categories_model.objects.all()


    def createProduct(self, data: dict):
        pass


    def getProduct(self):
        return self.product_model.objects.all()