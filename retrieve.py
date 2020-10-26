import os
import urllib.request

target_dir = "dependencies"
files = [{
    "filename": "compound-splitter-nl.tar.gz",
    "url": "https://ilps.science.uva.nl/ilps/wp-content/uploads/sites/6/files/compound-splitter-nl.tar.gz",
    "manual": True
}, {
    "filename": "secos.zip",
    "url": "https://github.com/riedlma/SECOS/archive/master.zip",
    "manual": False
}, {
    "filename": "secos-nl.zip",
    "url": "https://ltmaggie.informatik.uni-hamburg.de/files/SECOS/data.zip",
    "manual": True
}, {
    "filename": "MCS.jar", 
    "url": "https://www.ims.uni-stuttgart.de/documents/ressourcen/werkzeuge/MCSfiles/MCS.jar",
    "manual": False
}, {
    "filename": "MCS_lemmaset.tsv",
    "url": "https://www.ims.uni-stuttgart.de/documents/ressourcen/werkzeuge/MCSfiles/Wikipedia.NL.LEMMASET.tsv",
    "manual": False
}, {
    "filename": "MCS_mopset.tsv",
    "url": "https://www.ims.uni-stuttgart.de/documents/ressourcen/werkzeuge/MCSfiles/Wikipedia.NL.WORDMOPs.tsv",
    "manual": False
}]

os.makedirs(target_dir, exist_ok=True)

for file in files:
    target = os.path.join(target_dir, file["filename"])
    if not os.path.exists(target):
        url = file["url"]

        request = urllib.request.Request(url)

        if file["manual"]:
            # server might require that a browser is used
            # for downloading
            input(
                f'Download {url} manually and place in {target}. Press ENTER when done.')
        else:
            print(f'Downloading {url}')
            response = urllib.request.urlopen(request)
            with open(target, "wb+") as target_file:
                target_file.write(response.read())
