import time

from Components import HallSensor
from _config import load_components_config
import visualization as vis


def main():
    components = load_components_config()

    hall = HallSensor(components.get('position').get('pos_y'))

    vis.print_title(f"Hall (Magnet) Sensor : {hall.name}")
    vis.print_subtitle(f"[Ctrl + C to exit]")
    print()

    try:
        while True:
            reading = hall.sense_magnet()
            context = f"Sensing Magnet : {'YES' if reading else 'No '}"
            vis.print_context_update(context)

            time.sleep(0.25)
        
    except KeyboardInterrupt:
        vis.exit_terminal_menu(prompt=f"Hall (Magnet) Sensor ended.")
        exit(0)


if __name__ == "__main__":
    main()