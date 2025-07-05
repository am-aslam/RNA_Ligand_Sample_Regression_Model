import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
import numpy as np

# Sample ML placeholder
def mock_predict_class(features):
    return "Binding" if features["MolWt"] < 500 else "Non-Binding"

def mock_predict_affinity(features):
    return round(7.5 - (features["MolWt"] / 1000), 2)

# Feature extraction from SMILES (simple version)
def extract_ligand_features(smiles):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return {
        "MolWt": Descriptors.MolWt(mol),
        "LogP": Descriptors.MolLogP(mol),
        "NumHDonors": Descriptors.NumHDonors(mol),
        "NumHAcceptors": Descriptors.NumHAcceptors(mol)
    }

# Streamlit app
st.title("🧬 RNA–Ligand Interaction Prediction")

tab1, tab2, tab3 = st.tabs(["🔍 Predict Interaction", "📊 View Features", "📁 Browse Database"])

with tab1:
    st.header("🔍 Predict RNA–Ligand Binding")
    smiles_input = st.text_input("Enter Ligand SMILES", "CCO")
    rna_motif = st.selectbox("Select RNA Structural Motif", ["Hairpin", "Bulge", "Internal Loop", "Pseudoknot"])
    
    if st.button("Predict Interaction"):
        features = extract_ligand_features(smiles_input)
        if features:
            classification = mock_predict_class(features)
            affinity = mock_predict_affinity(features)
            st.success(f"🧪 Prediction: {classification}")
            st.info(f"📈 Predicted Affinity Score: {affinity}")
        else:
            st.error("Invalid SMILES string. Please enter a valid molecule.")

with tab2:
    st.header("📊 Ligand Feature Extraction")
    smiles_view = st.text_input("Enter SMILES to View Features", "CCO")
    features = extract_ligand_features(smiles_view)
    if features:
        st.write(pd.DataFrame([features]))
    else:
        st.warning("Invalid SMILES string.")

with tab3:
    st.header("📁 Sample RNA–Ligand Database")
    data = {
        "RNA Motif": ["Hairpin", "Bulge", "Loop"],
        "Ligand SMILES": ["CCO", "CCCC", "c1ccccc1"],
        "Binding": ["Yes", "No", "Yes"]
    }
    df = pd.DataFrame(data)
    st.dataframe(df)