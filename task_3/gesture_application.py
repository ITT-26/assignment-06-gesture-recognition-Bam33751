# gesture input program for first task
import time as time
import pyglet
import xml.etree.ElementTree as ET
from tqdm import tqdm
from recognizer import DollarRecognizer, Point
import os
import sys
sys.path.append("task_1")

GESTURES_TO_TRAIN = ['rectangle', 'circle', 'check', 'delete_mark', 'pigtail']
XML_LOGS_DIR = 'xml_logs'
XML_LOGS_OWN = 'datasets'
NUMBER_OF_POINTS = 64


def train_recognizer(recognizer):
    for root, subdirs, files in os.walk(XML_LOGS_DIR):
        for f in tqdm(files):
            if '.xml' in f:
                fname = f.split('.')[0]
                label = fname[:-2]
                if label not in GESTURES_TO_TRAIN:
                    continue

                xml_root = ET.parse(f'{root}/{f}').getroot()

                points = []
                for element in xml_root.findall('Point'):
                    x = element.get('X')
                    y = element.get('Y')
                    points.append(Point(float(x), float(y)))

                recognizer.addGesture(label, points)


def get_next_file_name(name):
    # Made With ChatGPT
    existing_files = [f for f in os.listdir(
        XML_LOGS_OWN) if f.startswith(name) and f.endswith('.xml')]
    if not existing_files:
        return f"{name}_01.xml"

    max_index = 0
    for f in existing_files:
        try:
            index = int(f.split('_')[-1].split('.')[0])
            max_index = max(max_index, index)
        except ValueError:
            continue

    return f"{name}_{max_index + 1:02d}.xml"


class GestureInputApp:
    def __init__(self):
        self.recognizer = DollarRecognizer()
        train_recognizer(self.recognizer)
        self.width = 800
        self.height = 800
        self.points = []
        self.font_factor = 0.03
        self.draw_points = []
        self.timestamps = []
        self.result = None
        self.gesture_label = pyglet.text.Label('Start to draw a gesture', font_size=int(
            self.width * self.font_factor), x=0 + self.width * 0.05, y=self.height - (self.height * 0.1))
        self.window = pyglet.window.Window(self.width, self.height)

    def on_draw(self):
        self.window.clear()
        self.gesture_label.draw()
        if len(self.points) < 2:
            return
        coords = []
        for p in self.draw_points:
            coords.append((p.x, p.y))
        line = pyglet.shapes.MultiLine(*coords, thickness=2, color=(255, 0, 0))
        line.draw()

    def append_points(self, x, y):
        t = int(time.time() * 1000)

        point_to_add = Point(x, self.height - y)

        if len(self.points) > 0:
            last_point = self.points[-1]

            if point_to_add.x == last_point.x and point_to_add.y == last_point.y:
                return

        self.points.append(point_to_add)
        self.draw_points.append(Point(x, y))
        self.timestamps.append(t)

    def recognize(self):
        if len(self.points) < 2:
            return
        points_copy = self.points.copy()
        result = self.recognizer.recognize(points_copy, useProtractor=True)
        print(" Recognized gesture: ", result.name,
              " with score: ", result.score)
        self.result = result
        self.gesture_label.text = f"Recognized: {result.name} with {result.score * 100:.2f}% confidence"

    def on_mouse_press(self, x, y, button, modifiers):
        self.points = []
        self.draw_points = []
        self.timestamps = []
        self.append_points(x, y)

    def save_gesture(self):
        if self.result is None:
            return

        os.makedirs(XML_LOGS_OWN, exist_ok=True)

        name = self.result.name
        root = ET.Element("Gesture", {
            "Name": name,
            "NumPts": str(len(self.points))
        })
        for i, p in enumerate(self.points):
            point_element = ET.SubElement(root, "Point")
            point_element.set("X", str(p.x))
            point_element.set("Y", str(p.y))
            point_element.set("T", str(self.timestamps[i]))

        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ")
        tree.write(f"{XML_LOGS_OWN}/{get_next_file_name(name)}",
                   encoding='utf-8', xml_declaration=True)


def main():
    app = GestureInputApp()

    @app.window.event
    def on_draw():
        app.on_draw()

    @app.window.event
    def on_mouse_press(x, y, button, modifiers):
        app.on_mouse_press(x, y, button, modifiers)
        pass

    @app.window.event
    def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
        app.append_points(x, y)
        pass

    @app.window.event
    def on_mouse_release(x, y, buttons, modifiers):
        app.append_points(x, y)
        app.recognize()
        pass

    @app.window.event
    def on_key_press(symbol, modifiers):
        if symbol == pyglet.window.key.ESCAPE:
            pyglet.app.exit()
        if symbol == pyglet.window.key.S:
            app.save_gesture()

    pyglet.app.run()


if __name__ == '__main__':
    main()
