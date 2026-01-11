import streamlit as st
import zipfile
import io
#Le Titre de la page
st.header("Modification automatique de fichier HTML")

# Upload d’un fichier ZIP 
uploaded_zip = st.file_uploader(
    "Importer un fichier ZIP contenant des fichiers HTML",
    type=["zip"]
)

# Les balises à modifier
replacements = {
    "[EMAIL]": "#A7_email#",
    "[PRENOM]": "#A7_prenom#",
    "[NOM]": "#A7_nom#",
    "[NOMDELABASE]": "#A7_platformreference#",
}

if uploaded_zip is not None and st.button("Analyser et Modifier"):  # si le dossier n'est pas vide 

    # Lire le dossier ZIP
    zip_bytes = uploaded_zip.read()
    # Transformer le fichier zip en  fichier exploitable par python
    zip_buffer = io.BytesIO(zip_bytes)
    # Ouverture de fichier zip en mode lecture
    with zipfile.ZipFile(zip_buffer, "r") as zip_file:
        #récupération des noms des fichiers existant dans le zip dans une liste
        file_list = zip_file.namelist()
        st.subheader("Fichiers dans le ZIP :")
        # Affichage des noms de fichiers 
        st.write(file_list)

        # Créer un nouveau ZIP pour les fichiers modifiés
        zip_modified_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_modified_buffer, "w", zipfile.ZIP_DEFLATED) as new_zip:
            for file_name in file_list:
                # Lire le contenu du fichier
                with zip_file.open(file_name) as f:
                    content = f.read().decode("utf-8")  # texte

                    # Modifier le contenu si besoin
                    modified_content = content
                    for old, new in replacements.items():
                        modified_content = modified_content.replace(old, new)

                    # Ajouter le fichier modifié dans le nouveau ZIP
                    new_zip.writestr(file_name, modified_content)

        zip_modified_buffer.seek(0)
        st.success("Modification terminée ✅")
        # Bouton pour télécharger le ZIP modifié
        st.download_button(
            label="Télécharger le ZIP des fichiers modifiés",
            data=zip_modified_buffer,
            file_name=uploaded_zip.name,
            mime="application/zip"
        )
        
