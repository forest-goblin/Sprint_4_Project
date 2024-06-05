import streamlit as st
from json import load

filename = 'EDA.ipynb'
with open(filename) as fp:
    nb = load(fp)