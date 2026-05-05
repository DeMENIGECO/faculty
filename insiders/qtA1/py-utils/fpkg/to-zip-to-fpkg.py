import zipfile
import os
import shutil
import tempfile
import xml.etree.ElementTree as ET

# Fix per doppio click
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Input zip
zip_path = input("Inserisci il file .zip: ").strip()

if not zip_path.endswith(".zip"):
    print("Errore: devi inserire un file .zip")
    input("Premi INVIO per chiudere...")
    exit()

# 2. Cartella temporanea
temp_dir = tempfile.mkdtemp()

# 3. Estrazione zip
try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
except zipfile.BadZipFile:
    print("Errore: ZIP non valido")
    input("Premi INVIO per chiudere...")
    exit()

# 4. Trova manifest.xml
manifest_path = None

for root, dirs, files in os.walk(temp_dir):
    for f in files:
        if f == "manifest.xml":
            manifest_path = os.path.join(root, f)

if not manifest_path:
    print("Errore: manifest.xml non trovato")
    input("Premi INVIO per chiudere...")
    exit()

# 5. Leggi nome pacchetto
tree = ET.parse(manifest_path)
root = tree.getroot()

package_name = root.find(".//name").attrib["content"]
print("Nome pacchetto:", package_name)

# 6. Ricrea archivio ZIP interno
output_zip = os.path.join(temp_dir, package_name + ".zip")

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root_dir, dirs, files in os.walk(temp_dir):
        for file in files:
            full_path = os.path.join(root_dir, file)

            if full_path == output_zip:
                continue

            arcname = os.path.relpath(full_path, temp_dir)
            zipf.write(full_path, arcname)

# 7. Rinominazione in .fpkg
fpkg_file = os.path.join(os.getcwd(), package_name + ".fpkg")
shutil.copy(output_zip, fpkg_file)

print("Conversione completata!")
print("File creato:", fpkg_file)

input("Premi INVIO per chiudere...")