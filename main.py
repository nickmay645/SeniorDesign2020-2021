from services import ThermalDetection

if __name__ == "__main__":
    instance = ThermalDetection.ThermalDetection()
    # Init has run

    instance.initialize_servos()
    instance.initialize_vis_camera()
    instance.run()
