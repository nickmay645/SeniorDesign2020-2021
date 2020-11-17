from services import ThermalDetection

if __name__ == "__main__":

    instance = ThermalDetection.ThermalDetection()
    # Init has run


    instance.initializeServos()
    instance.initializeCamera()
    instance.run()


