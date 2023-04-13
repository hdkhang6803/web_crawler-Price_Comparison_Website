from flask import Flask, render_template, send_from_directory, request, jsonify

from DataStructures.GoogleSheet import GoogleSheet
from DataStructures.ProductClassifier import ProductClassifier
from DataStructures.SearchEngine import SearchEngine

spreadsheet_id = '1H5TTOdrTC_T7U7k_ejCUG8BZWn97NuaxD0t4F7LwH8g'
cred_file = 'client_secret.json'

app = Flask(__name__, template_folder="./frontend/")

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/<path:filepath>')
def sendDirCss(filepath):
    return send_from_directory('frontend/', filepath)

def get_page_name(productLink):
    page = {
        "phongvu": "PHONG VŨ",
        "tiki": "TIKI", 
        "cellphones": "CELLPHONES",
        "fpt": "FPT",
        "hacom": "HACOM",
        "tgdd": "THẾ GIỚI DI ĐỘNG"
        }

    for x in list(page.keys()):
        if (x in productLink):
            return page[x]
    return ""

@app.route('/getProducts')
def get_products():
    user_input = request.args.get("q")

    result = searchEngine.search_product(user_input)
    print(result)
    best_product = result[0][1]
    good_products = [x[1] for x in result[1:]]
    product_divs = [render_template('best_product.html', title = best_product[0], price = best_product[1], product_link = best_product[2], img_link = best_product[3], page_name = get_page_name(best_product[2]))]
    # product_divs =  product_divs.append([render_template('product.html', title = product[0], price = product[1], product_link=product[2], img_link=product[3]) for product in good_products])
    for product in good_products:
        product_divs.append(render_template('product.html', title = product[0], price = product[1], product_link=product[2], img_link=product[3], page_name = get_page_name(product[2])))

    return jsonify(product_divs)

if __name__ == "__main__":
    global searchEngine
    ggsheet = GoogleSheet(spreadsheet_id, cred_file)
    classifier = ProductClassifier(spreadsheet_id, cred_file)
    if (classifier.load_model()):
        print("model loaded succesfully yay")
        # print(classifier.predict("Laptop ASUS"))
    else:
        classifier.train_classifier()
        classifier.get_accuracy()
        # print(classifier.predict("Laptop ASUS"))
        classifier.save_model()
    searchEngine = SearchEngine(classifier= classifier, spreadsheet_id= spreadsheet_id, cred_file= cred_file,
                                brand_file= "brand_names.txt")
    app.run(debug = True)