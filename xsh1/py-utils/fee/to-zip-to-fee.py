import zipfile
import os
import shutil
import tempfile
import xml.etree.ElementTree as ET


os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Input file zip
zip_path = input("Inserisci il file .zip: ").strip()

if not zip_path.endswith(".zip"):
    print("Errore: devi inserire un file .zip")
    exit()

# 2. Cartella temporanea
temp_dir = tempfile.mkdtemp()

# 3. Estrazione zip
with zipfile.ZipFile(zip_path, 'r') as zip_ref:
    zip_ref.extractall(temp_dir)

# 4. Trova manifest.xml
manifest_path = None
files_path = None

for root, dirs, files in os.walk(temp_dir):
    for f in files:
        if f == "manifest.xml":
            manifest_path = os.path.join(root, f)
        if f == "files.xml":
            files_path = os.path.join(root, f)

if not manifest_path or not files_path:
    print("manifest.xml o files.xml non trovati")
    exit()

# 5. Parsing manifest.xml → nome pacchetto
tree = ET.parse(manifest_path)
root = tree.getroot()

package_name = root.find(".//name").attrib["content"]
print("Nome pacchetto:", package_name)

# 6. Parsing files.xml → regole
tree2 = ET.parse(files_path)
root2 = tree2.getroot()

rules = []

for file_ext in root2.findall(".//file-ext"):
    rule = {
        "extension": file_ext.attrib.get("extension"),
        "correspond": file_ext.attrib.get("correspond"),
        "dir": file_ext.attrib.get("dir")
    }
    rules.append(rule)

print("Regole caricate:", rules)

# 7. Spostamento file
for root_dir, dirs, files in os.walk(temp_dir):
    for file in files:
        file_path = os.path.join(root_dir, file)

        for rule in rules:
            ext = rule["extension"].replace("*", "")

            if file.endswith(ext):
                target_dir = os.path.join(temp_dir, rule["dir"])
                os.makedirs(target_dir, exist_ok=True)

                shutil.move(file_path, os.path.join(target_dir, file))
                break

# 8. Creazione nuovo zip
output_zip = os.path.join(temp_dir, package_name + ".zip")

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root_dir, dirs, files in os.walk(temp_dir):
        for file in files:
            full_path = os.path.join(root_dir, file)

            # evita di zippare il zip stesso
            if full_path == output_zip:
                continue

            arcname = os.path.relpath(full_path, temp_dir)
            zipf.write(full_path, arcname)

# 9. Rename a .fee
fee_file = output_zip.replace(".zip", ".fee")
shutil.copy(output_zip, fee_file)

# 10. Copia nella directory dello script
final_path = os.path.join(os.getcwd(), os.path.basename(fee_file))
shutil.copy(fee_file, final_path)

print("Completato!")
print("File creato:", final_path)

input("Premi INVIO per chiudere")