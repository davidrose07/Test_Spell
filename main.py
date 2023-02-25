from controller import *

def main() -> None:
    application = QApplication([])
    window=Controller()
    application.exec_()

if __name__ == "__main__": 
    main()
    
