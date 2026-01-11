import streamlit as st
import zipfile
import io

st.title("HTML Automator - Custom Tag Replacement")

# Import ZIP
uploaded_zip = st.file_uploader("Upload a ZIP containing HTML files", type=["zip"])

# Zone pour balises à remplacer et leurs remplacements
st.subheader("Enter the tags to replace and their replacements")

# L'utilisateur entre les balises sous forme de liste : "balise1=remplacement1, balise2=remplacement2"
tags_input = st.text_area(
    "Format: old_tag1=new_tag1, old_tag2=new_tag2",
    placeholder="Example: [NAME]=John,[EMAIL]=example@example.com"
)

if st.button("Analyze & Modify") and uploaded_zip is not None and tags_input:
    
    # Créer le dictionnaire de remplacements à partir de la saisie utilisateur
    replacements = {}
    for pair in tags_input.split(","):
        if "=" in pair:
            old, new = pair.split("=")
            replacements[old.strip()] = new.strip()

    # Lire le ZIP
    zip_bytes = uploaded_zip.read()
    zip_buffer = io.BytesIO(zip_bytes)
    
    with zipfile.ZipFile(zip_buffer, "r") as zip_file:
        # Créer un nouveau ZIP en mémoire
        zip_modified_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_modified_buffer, "w", zipfile.ZIP_DEFLATED) as new_zip:
            for file_name in zip_file.namelist():
                with zip_file.open(file_name) as f:
                    content = f.read().decode("utf-8")
                    # Remplacer les balises
                    modified_content = content
                    for old, new in replacements.items():
                        modified_content = modified_content.replace(old, new)
                    # Ajouter le fichier modifié au nouveau ZIP
                    new_zip.writestr(file_name, modified_content)

        # Repositionner le curseur pour le téléchargement
        zip_modified_buffer.seek(0)

        st.success("Files modified successfully ✅")
        st.download_button(
            label="Download Modified ZIP",
            data=zip_modified_buffer,
            file_name="modified_files.zip",
            mime="application/zip"
        )

        
