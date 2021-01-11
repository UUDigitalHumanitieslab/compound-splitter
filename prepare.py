from compound_splitter.splitter import list_methods, get_method

for method in list_methods():
    get_method(method["name"]).prepare()
