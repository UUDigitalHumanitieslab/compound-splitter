import os
import urllib.request

target_dir = "dependencies"
files = [{
    "filename": "compound-splitter-nl.tar.gz",
    "url": "https://ilps.science.uva.nl/ilps/wp-content/uploads/sites/6/files/compound-splitter-nl.tar.gz",
    "manual": True
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
