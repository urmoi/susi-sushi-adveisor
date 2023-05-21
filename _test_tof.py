import time

from Components import ToFDistanceSensor
from config import load_components_config, load_dimensions_config
import visualization as vis


def main():
    components = load_components_config()
    dimensions = load_dimensions_config()

    tof = ToFDistanceSensor(components.get('position').get('pos_x'))

    vis.print_title(f"ToF (Time of Flight) Sensor : {tof.name}")
    vis.print_subtitle(f"[Ctrl + C to exit]")

    try:
        offset = dimensions['offset']['x']
        while True:
            reading = tof.read_distance(offset)
            context = f"Distance : {reading:3} mm"
            if offset:
                context += f"   (offset: {offset:3} mm)"
            vis.print_context_update(context)

            time.sleep(0.25)
        
    except KeyboardInterrupt:
        vis.exit_terminal_menu(prompt=f"ToF (Time of Flight) Sensor ended.")
        exit(0)


if __name__ == "__main__":
    main()