import zipfile
import os
import shutil
import tempfile

# Assicura working directory corretta (utile per doppio click)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# 1. Input file .fee
fee_path = input("Inserisci il file .fee: ").strip()

if not fee_path.endswith(".fee"):
    print("Errore: devi inserire un file .fee")
    input("Premi INVIO per chiudere...")
    exit()

# 2. Cartella temporanea
temp_dir = tempfile.mkdtemp()

# 3. Tratta .fee come zip ed estrai
try:
    with zipfile.ZipFile(fee_path, 'r') as zip_ref:
        zip_ref.extractall(temp_dir)
except zipfile.BadZipFile:
    print("Errore: il file .fee non è un archivio valido")
    input("Premi INVIO per chiudere...")
    exit()

# 4. Recupera nome base dal file fee
base_name = os.path.splitext(os.path.basename(fee_path))[0]

# 5. Crea nuovo ZIP
output_zip = os.path.join(temp_dir, base_name + ".zip")

with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root_dir, dirs, files in os.walk(temp_dir):
        for file in files:
            full_path = os.path.join(root_dir, file)

            # evita di includere il zip stesso
            if full_path == output_zip:
                continue

            arcname = os.path.relpath(full_path, temp_dir)
            zipf.write(full_path, arcname)

# 6. Copia finale accanto allo script
final_zip = os.path.join(os.getcwd(), base_name + ".zip")
shutil.copy(output_zip, final_zip)

print("Conversione completata!")
print("File creato:", final_zip)

input("Premi INVIO per chiudere...")