from jobhunting.credentails import vagasPassword, vagasUser, user, password
from jobhunting.Models.Infojobs import Infojobs
from jobhunting.Models.vagasCom import VagasCom
from jobhunting.controllers.vagasComController import searchVagasCom
from jobhunting.controllers.infojobsController import searchInfojob
import sys
import warnings


if not sys.warnoptions:
    warnings.simplefilter("ignore")


def main():
    # searchVagasCom('robot', vagasUser, vagasPassword, headless=True)
    searchInfojob('python', user, password, headless=True)
        

if __name__ == "__main__":
    main()
