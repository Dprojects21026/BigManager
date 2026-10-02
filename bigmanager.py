from kivy.uix.screenmanager import ScreenManager, Screen
class BigManager(ScreenManager):
    class ManagerAlreadyExist(Exception):
        pass
    class UnknownManager(Exception):
        pass

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        from kivy.uix.screenmanager import ScreenManager, Screen
        self.widgets_types = {}
        self.managers = []
        self._screens_ = []
        self.data = {}
    #unusable ScreenManager funks
    def add_widget(self, widget, *args, **kwargs):
        raise AttributeError("'add_widget()' is not allowed for using in `BigManager`, use 'add_manager()' or 'add_screen' instead")

    def remove_widget(self, widget, *args, **kwargs):
        raise AttributeError("'remove_widget()' is not allowed for using in `BigManager`, use 'remove_manager()' or 'remove_screen' instead")

    #BigManager funks
    def __ADD_WIDGET__(self, widget, name:str, widget_type:str, *args, **kwargs):
        if widget_type.lower() != "manager" and widget_type.lower() != "screen":
            raise TypeError("'widget_type' must be 'manager' or 'screen'.")
        self.widgets_types[name] = widget_type.lower()
        self.data[name] = {}
        if widget_type.lower() == "manager":
            self.managers.append(name)
        else:
            self._screens_.append(name)
        super().add_widget(widget, *args, **kwargs)

    def __REMOVE_WIDGET__(self, widget, name:str, *args, **kwargs):
        del self.widgets_types[name]
        super().remove_widget(widget, *args, **kwargs)

    def add_manager(self, manager_name, manager):
        if type(manager_name) != str:
            raise TypeError(f"Unusable manager_name type: {type(manager_name)}, use 'str'('')")
        if hasattr(self, manager_name):
            raise BigManager.ManagerAlreadyExist(f"Manager with name '{manager_name}' already exists, use other name!")
        setattr(self, manager_name, Screen(name=manager_name))
        screen: Screen = getattr(self, manager_name)
        screen.add_widget(manager)
        screen.inner_manager = manager
        self.__ADD_WIDGET__(screen,name=manager_name,widget_type="manager")

    def add_screen(self, screen_name, screen):
        screen = screen(name=screen_name)
        setattr(self, screen_name, screen)
        self.__ADD_WIDGET__(
            screen,
            name=screen_name,
            widget_type="screen"
        )

    def remove_manager(self, manager_name):
        if not hasattr(self, manager_name) or manager_name not in self.managers:
            raise BigManager.UnknownManager(f"Manager with name '{manager_name}' does not exist.Exist managers:\n", self.managers,"\n",self.children)
        self.__REMOVE_WIDGET__(getattr(self, manager_name),manager_name)
        delattr(self, manager_name)
        self.managers.remove(manager_name)

    def remove_screen(self, screen_name):
        self.__REMOVE_WIDGET__(getattr(self, screen_name), screen_name)
        delattr(self, screen_name)
        self._screens_.remove(screen_name)

    def current_manager(self, manager_name):
        if manager_name not in self.managers and not hasattr(self, manager_name):
            raise BigManager.UnknownManager(f"Manager with name '{manager_name}' does not exist.Exist managers:\n", self.managers)
        self.current = manager_name

    def current_screen(self, screen_name, manager_name = None):
        if not hasattr(self, manager_name) and manager_name is not None:
            raise BigManager.UnknownManager(f"Manager with name '{manager_name}' does not exist.Exist managers:\n", self.managers)
        if manager_name is not None:
            self.current = manager_name
        if manager_name is None:
            manager_name = self.current
        getattr(self, manager_name).inner_manager.current = screen_name

    def save_data(self, manager_name, data_key, data):
        self.data[manager_name][data_key] = data

    def get_data(self, manager_name, data_key):
        if data_key not in self.data[manager_name]:
            return None
        return self.data[manager_name][data_key]

