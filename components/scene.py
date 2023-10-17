class Scene(): pass

from components.element import *

class Scene():
    all_elements: set[Element] = set()

    def get_element_by_id(self, id: str):
        for element in self.all_elements:
            if element.id == id:
                return element