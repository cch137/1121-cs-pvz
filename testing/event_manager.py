from ..components import *

def test_event_manager():
    x = Element((1,2))

    def xOnClick1(e):
        print('x on click 1')

    def xOnClick2():
        print('x on click 2')

    x.add_event_listener('click', xOnClick1)
    x.add_event_listener('click', xOnClick2)

    x.dispatch_event(event_manager.events.ClickEvent((0,0)))

test_event_manager()