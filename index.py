from jobhunting.credentails import vagasPassword, vagasUser, user, password
from jobhunting.Models.Infojobs import Infojobs
from jobhunting.Models.vagasCom import VagasCom
from jobhunting.controllers.vagasComController import searchVagasCom
from jobhunting.controllers.infojobsController import searchInfojob
import sys


def main():
    # searchVagasCom('robot', vagasUser, vagasPassword, headless=True)
    searchInfojob('robot', user, password, headless=False)
        

if __name__ == "__main__":
    main()
