from services import ThermalDetection

if __name__ == "__main__":

    instance = ThermalDetection.ThermalDetection()
    instance.initializeServos()
    instance.initializeCamera()
    instance.run()


