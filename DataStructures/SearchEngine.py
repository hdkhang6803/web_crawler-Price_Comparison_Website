# from ProductClassifier import ProductClassifier
from DataStructures.CappedPriorityQueue import CappedPriorityQueue
from DataStructures.GoogleSheet import GoogleSheet

# TODO: restructure class so that it would be reusable

class SearchEngine:
    def __init__(self, classifier, spreadsheet_id, cred_file, brand_file, calc_point_func = None):
        self.__brands__ = self.get_brand_names(brand_file)
        if (calc_point_func == None):
            self.calc_point_func = self.calc_point
        else:
            self.calc_point_func = calc_point_func
        self.classifier = classifier
        self.ggsheet = GoogleSheet(spreadsheet_id, cred_file)
        pass

    def get_brand_names(self, brand_file):
        brand_names = []
        with open(brand_file, "r") as f:
            brand_names = f.readlines()
        brand_names = [x.strip().lower() for x in brand_names]
        return brand_names

    def value_of_queue_item(self, point_obj):
        return point_obj[0]

    def calc_point(self, user_input, product):
        user_input = user_input.lower().split()
        product = product.lower().split()
        matched = 0
        total = 0

        total = len(user_input)
        for str in user_input:
            if (str in self.__brands__):
                if (str not in product):
                    matched -= 5
            if (str in product):
                matched += 1

        return matched / total

    def search_product(self, user_input):
        category = self.classifier.predict(user_input)
        print(category)

        data = self.ggsheet.get_data(1, 1000, 4, category)['values']

        chosen_products = CappedPriorityQueue(self.value_of_queue_item, 6)
        for row in data:
            if (chosen_products.good(0.8)):
                break
            else:
                point_obj = [self.calc_point_func(user_input, row[0]), row]
                chosen_products.push(point_obj)
            
            # print(" ----------------------- ")
            # chosen_products.print()

        return chosen_products.arr

    