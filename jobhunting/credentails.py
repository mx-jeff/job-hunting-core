"""
Credentials Infojobs here, replace the following line below
"""
import os
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get('USER') 
password = os.environ.get('PASSWORD') 

vagasUser = os.environ.get('VAGAS_USER') 
vagasPassword = os.environ.get('VAGAS_PASSWORD') 
