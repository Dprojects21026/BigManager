import os
import random
import copy
from color_text import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from datetime import datetime
import json
from pathlib import Path
import shutil


def create_json_file(path: str, parent_count: int = 0):
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")
    if Path(path).suffix.lower() != ".json":
        raise ValueError("File must have a '.json' extension.")

    file_path = create_file(path, parent_count)

    if file_path.stat().st_size == 0:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump({}, f)

    return file_path

def create_file(path: str, parent_count: int = 0):
    if not isinstance(path, str):
        raise TypeError("Path must be a string.")
    if not isinstance(parent_count, int) or isinstance(parent_count, bool):
        raise TypeError("parent_count must be an integer.")
    if parent_count < 0:
        raise ValueError("parent_count cannot be negative.")

    file_path = Path(__file__).resolve()

    for _ in range(parent_count):
        file_path = file_path.parent

    file_path = file_path / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    file_path.touch(exist_ok=True)

    return file_path

def can_access_file(path: str | Path) -> bool:
    try:
        path = Path(path)

        if not path.is_file() or path.suffix.lower() != ".json":
            return False

        for parent in path.parents:
            if not os.access(parent, os.X_OK):
                return False

        return os.access(path, os.R_OK)

    except (OSError, ValueError, TypeError):
        return False

def is_folder_empty(path: str | Path) -> bool:
    path = Path(path)
    return path.is_dir() and not any(path.iterdir())

def clear_folder(path: str | Path) -> None:
    path = Path(path)

    if not path.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    for item in path.iterdir():
        if item.is_dir() and not item.is_symlink():
            shutil.rmtree(item)
        else:
            item.unlink()

def remove_file(path: str | Path) -> bool:
    path = Path(path)

    if path.is_file():
        path.unlink()
        return True

    return False

def create_folder(path: str | Path) -> bool:
    path = Path(path)

    if path.exists():
        return False

    path.mkdir(parents=True)
    return True

class BigManager(ScreenManager):
    utils = {
        "BigManagers exist": 0,
        "BigManagers ids": [],
        "global data": {}
    }
    with open(Path(__file__).parent / "BigManager`s util.json", "w") as file:
        json.dump(utils, file)
    del utils

    class Errors(Exception):
        pass

    def __init__(self, name: str, **kwargs):
        if not isinstance(name, str):
            raise TypeError("Name must be a string")
        if "\n" in name:
            raise BigManager.Errors(f"Attribute 'name' can`t include '\\n'!")
        name = name.strip()
        super().__init__(**kwargs)

        def gen_id():
            id = "BigManager_"
            for i in range(5):
                symb = random.choice([
                    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u", "v", "w", "x", "y", "z"
                ])
                caps = random.choice([True, False])
                _int = random.choice([True, False])
                if caps:
                    symb = symb.upper()
                if _int:
                    symb = str(random.randint(0, 9))
                id += symb
            return id

        self.id = gen_id()
        self.util_path = Path(__file__).parent / "BigManager`s util.json"

        with open(self.util_path, "r") as file:
            utils = json.load(file)

        if name and name in utils["global data"]:
            raise BigManager.Errors(
                f"BigManager with name '{name}' already exists."
            )

        while self.id in utils["BigManagers ids"]:
            self.id = gen_id()

        utils["BigManagers exist"] += 1
        utils["BigManagers ids"].append(self.id)
        self.name = name

        if name == "":
            index = utils["BigManagers exist"]
            self.name = f"Random_BigManager_name_{index}"

            while self.name in utils["global data"]:
                index += 1
                self.name = f"Random_BigManager_name_{index}"

        utils["global data"][self.name] = {}

        with open(self.util_path, "w", encoding="utf-8") as file:
            json.dump(utils, file)

        self.managers = []
        self._screens_ = []
        self.manager = None
        self.data = DataManager(name=f"{self.name}_DataManager")
        self.deleted_widgets = []

    # unusable ScreenManager funks
    def add_widget(self, widget, *args, **kwargs):
        raise AttributeError(
            "'add_widget()' is not allowed for using in `BigManager`, use 'add_manager()' or 'add_screen' instead"
        )

    def remove_widget(self, widget, *args, **kwargs):
        raise AttributeError(
            "'remove_widget()' is not allowed for using in `BigManager`, use 'add_manager()' or 'add_screen' instead"
        )

    # BigManager funks
    @staticmethod
    def contains_bigmanager(widget):
        if isinstance(widget, BigManager):
            return True

        inner_manager = getattr(widget, "inner_manager", None)

        if isinstance(inner_manager, BigManager):
            return True

        for child in getattr(widget, "children", []):
            if BigManager.contains_bigmanager(child):
                return True

        return False

    def print_info(self, got_from=None, **kwargs):
        _color_ = kwargs.get("Color(", "green")
        bright = kwargs.get("bright", False)
        will_print = True
        _space_ = " "

        with open(self.util_path, "r", encoding="utf-8") as file:
            utils = json.load(file)

        if got_from is not None:
            if got_from in utils["BigManagers ids"]:
                will_print = False

        if will_print:
            print(
                Color("-", False, ready_color="yellow") * 10,
                Color(
                    f"'{self.name}'`s info",
                    False,
                    ready_color="yellow"
                ),
                Color("-", False, ready_color="yellow") * 10,
                sep=""
            )

        print(
            Color(
                text=f"{_space_}Name: '{self.name}'",
                rgb_sys=False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                text=f"{_space_}ID: '{self.id}'",
                rgb_sys=False,
                ready_color="red"
            )
        )

        if self.manager is not None:
            print(
                Color(
                    text=f"{_space_}Connected to: {self.manager.name}",
                    rgb_sys=False,
                    ready_color="blue"
                )
            )
        else:
            print(
                Color(
                    text=f"{_space_}Still not connected to any ConnectionManager....",
                    rgb_sys=False,
                    ready_color="red"
                )
            )

        print(
            Color(
                text=f"{_space_}Item count: {len(self.data.data.keys())}",
                rgb_sys=False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                text=f"{_space_}Current: {self.current}",
                rgb_sys=False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                text=f"{_space_}Managers: {self.managers}",
                rgb_sys=False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                f"{_space_}Screens: {self._screens_}",
                False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                f"{_space_}data: {self.data.data}",
                False,
                ready_color=_color_,
                bright=bright
            )
        )
        print(
            Color(
                f"{_space_}ScreenManagers` screens: {self.get_managers_screens()}",
                False,
                ready_color=_color_,
                bright=bright
            )
        )

        if will_print:
            print(
                Color("-" * 10, False, ready_color="yellow"),
                Color(
                    f"'{self.name}'`s info",
                    False,
                    ready_color="yellow"
                ),
                Color("-" * 10, False, ready_color="yellow"),
                sep=""
            )

    def get_managers_screens(self):
        return_data = {}

        for _manager in self.managers:
            _manager_ = getattr(self, _manager)
            children = _manager_.inner_manager.children
            return_data[_manager] = children

        return return_data

    def get_date(self, part=None, int_part=None):
        if not part:
            part = "all"

        if int_part is not None:
            if type(int_part) is not int:
                raise AttributeError(f"'{int_part}' is not an 'int' object!")

        if not isinstance(part, str):
            raise AttributeError(f"'{part}' is not an 'str' object!")

        now = datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
        second = now.second
        millisecond = now.microsecond // 1000
        microsecond = now.microsecond - 1000 * (now.microsecond // 1000)

        date = {
            "date": {
                1: f"{day}/{month}/{year}",
                2: f"{day}/{month}"
            },
            "direct date": f"{day}/{month}/{year} {hour}:{minute}:{second}.{millisecond}",
            "time": f"{hour}:{minute}",
            "direct time": {
                1: f"{hour}:{minute}:{second}",
                2: f"{hour}:{minute}:{second}.{millisecond}",
                3: f"{hour}:{minute}:{second}.{millisecond}.{microsecond}"
            },
            "year": year,
            "month": month,
            "day": day,
            "hour": hour,
            "minute": minute,
            "second": second,
            "millisecond": millisecond,
            "microsecond": {
                1: microsecond,
                2: now.microsecond
            }
        }

        if part not in date:
            return None, f"'{part}' is not a valid key of 'date'. Available keys: {date.keys()}."

        if int_part is None:
            return date[part], "Got successfully."

        if int_part is not None and type(date[part]) != dict:
            return None, f"'{part}' is not a dict. {part}: {date[part]}"

        if int_part not in date[part]:
            return None, f"'{int_part}' is not a valid key for '{part}'. Available keys: {date[part].keys()}."

        return date[part][int_part], "Got successfully."

    def __ADD_WIDGET__(
            self,
            widget,
            name: str,
            *args,
            **kwargs
    ):
        if not isinstance(name, str):
            raise TypeError("Widget name must be a string.")

        if not name:
            raise BigManager.Errors("Widget name cannot be empty.")

        if name in self.data.data:
            raise BigManager.Errors(f"Widget '{name}' already exists.")

        if isinstance(widget, Screen):
            if isinstance(getattr(widget, "inner_manager", None), ScreenManager):
                widget_type = "manager"
            else:
                widget_type = "screen"
        else:
            raise BigManager.Errors(f"Widget '{name}' is not a Screen.")

        if self.contains_bigmanager(widget):
            raise TypeError(
                "Adding a screen containing a BigManager is not allowed."
            )

        super().add_widget(widget, *args, **kwargs)

        self.data.data[name] = {}

        if widget_type.lower() == "manager":
            self.managers.append(name)

            for child in widget.inner_manager.screens:
                self.data.data[name][child.name] = {}

        else:
            self._screens_.append(name)

    def __REMOVE_WIDGET__(self, widget, name: str, *args, **kwargs):
        if name not in self.data.data:
            raise BigManager.Errors(f"Key '{name}' not found.")

        if name not in self.managers and name not in self._screens_:
            raise BigManager.Errors(f"Widget '{name}' was not registered.")
        if getattr(self, name, None) is not widget:
            raise BigManager.Errors(
                f"The provided widget does not match the registered widget '{name}'."
            )

        # Сохраняем исходное состояние
        old_data = copy.deepcopy(self.data.data)
        old_managers = self.managers.copy()
        old_screens = self._screens_.copy()
        old_deleted_widgets = self.deleted_widgets.copy()

        with open(self.util_path, "r", encoding="utf-8") as file:
            old_json = file.read()

        utils = json.loads(old_json)
        global_data = utils["global data"].get(self.name, {})

        index = 1
        while (
                f"{name}_old_{index}" in self.data.data
                or f"{name}_old_{index}" in global_data
        ):
            index += 1

        old_name = f"{name}_old_{index}"
        self.deleted_widgets.append(old_name)

        try:
            # Удаляем виджет
            super().remove_widget(widget, *args, **kwargs)

            if name in self.managers:
                self.managers.remove(name)
            else:
                self._screens_.remove(name)

            # Переносим локальные данные
            self.data.data[old_name] = self.data.data.pop(name)

            # Переносим глобальные данные, если они существуют
            if name in global_data:
                global_data[old_name] = global_data.pop(name)

                with open(self.util_path, "w", encoding="utf-8") as file:
                    json.dump(utils, file, indent=4, ensure_ascii=False)

            print(
                Color(
                    text=f"[{self.name}][DATA]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Data '{name}' renamed to '{old_name}'.",
                    rgb_sys=False,
                    ready_color="green"
                )
            )

        except Exception:
            # Восстанавливаем данные и списки
            self.data.data = old_data
            self.managers[:] = old_managers
            self._screens_[:] = old_screens
            self.deleted_widgets[:] = old_deleted_widgets

            # Восстанавливаем JSON-файл
            with open(self.util_path, "w", encoding="utf-8") as file:
                file.write(old_json)

            # Возвращаем виджет, если он был удалён
            if widget not in self.screens:
                super().add_widget(widget)

            raise

    def add_manager(self, manager, manager_name: str):
        if isinstance(manager, BigManager):
            raise TypeError("Adding Bigmanager into another one is not allowed.")

        if not isinstance(manager, ScreenManager):
            raise TypeError("Type of manager must be 'ScreenManager'.")

        if self.contains_bigmanager(manager):
            raise TypeError(
                "Adding a BigManager inside another BigManager is not allowed."
            )

        if not isinstance(manager_name, str):
            raise TypeError("Manager name must be a string.")

        manager_name = manager_name.strip()
        if manager_name == "":
            raise TypeError("Manager name must be set.")

        if hasattr(self, manager_name):
            raise BigManager.Errors(
                f"Object with name '{manager_name}' already exists, use other name!"
            )

        setattr(self, manager_name, Screen(name=manager_name))
        screen: Screen = getattr(self, manager_name)
        screen.add_widget(manager)
        screen.inner_manager = manager
        screen.bigmanager = self
        delattr(self, manager_name)

        self.__ADD_WIDGET__(
            screen,
            name=manager_name
        )
        setattr(self, manager_name, screen)

    def add_screen(self, screen: Screen, *args, **kwargs):
        if not isinstance(screen, Screen):
            raise TypeError("Type of screen must be 'Screen'.")

        if self.contains_bigmanager(screen):
            raise TypeError(
                "Adding a screen containing a BigManager is not allowed."
            )

        screen.name = screen.name.strip()

        if not screen.name:
            raise TypeError("Screen name must be set.")

        screen_name = screen.name

        if hasattr(self, screen_name):
            raise BigManager.Errors(
                f"Object with name '{screen_name}' already exists, use other name!"
            )

        screen.bigmanager = self

        self.__ADD_WIDGET__(
            screen,
            name=screen_name
        )

        setattr(self, screen_name, screen)

    def remove_manager(self, manager_name):
        if not hasattr(self, manager_name) or manager_name not in self.managers:
            raise BigManager.Errors(
                f"Manager '{manager_name}' does not exist. "
                f"Existing managers: {self.managers}"
            )

        self.__REMOVE_WIDGET__(getattr(self, manager_name), manager_name)
        delattr(self, manager_name)

    def remove_screen(self, screen_name):
        if not hasattr(self, screen_name) or screen_name not in self._screens_:
            raise BigManager.Errors(f"Screen with name '{screen_name}' does not exist.")
        self.__REMOVE_WIDGET__(getattr(self, screen_name), screen_name)
        delattr(self, screen_name)

    def connect(self, manager: "ConnectionManager"):
        if self.manager is not None:
            raise ConnectionManager.Errors("Manager already connected.")
        if not isinstance(manager, ConnectionManager):
            raise TypeError("Type of manager must be 'ConnectionManager'.")
        print(
            Color(
                text=f"[{self.name}][{manager.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Connecting...",
                rgb_sys=False,
                ready_color="blue"
            )
        )
        self.manager = manager
        print(
            Color(
                text=f"[{manager.name}][{self.name}][CONNECTING]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Connected successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )

    def disconnect(self):
        if not self.manager:
            raise ConnectionManager.Errors("Not connected to any ConnectionManager yet.")
        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Disconnecting from manager '{self.manager.name}'...",
                rgb_sys=False,
                ready_color="blue"
            )
        )
        self.manager = None
        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Disconnected successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )

    def switch_screen(self, screen_name: str, own: bool = True, manager_name: str = ""):
        self.set_current_screen(
            screen_name=screen_name,
            manager_name=manager_name,
            own=own
        )

    def set_current_screen(self, screen_name: str, own: bool = True, manager_name: str = ""):
        if not isinstance(screen_name, str):
            raise TypeError("Type of screen_name must be 'str'.")
        if not isinstance(manager_name, str):
            raise TypeError("Type of manager_name must be 'str'.")
        if not screen_name:
            raise TypeError("Screen name must be set.")

        manager_name = manager_name.strip()
        screen_name = screen_name.strip()

        if self.manager is None:
            own = True

        if own == False:
            self.manager.set_current_screen(
                screen_name=screen_name,
                manager_name=manager_name,
                got_from=self.name
            )
            return

        if manager_name != "":
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Finding manager with name '{manager_name}'...",
                    rgb_sys=False,
                    ready_color="blue"
                )
            )

            if manager_name not in self.managers:
                raise BigManager.Errors(f"Manager with name '{manager_name}' does not exist.")

            manager = getattr(self, manager_name).inner_manager

            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Manager with name '{manager_name}' was found and set successfully.",
                    rgb_sys=False,
                    ready_color="green"
                ),
                Color(
                    text=f"Finding screen with name '{screen_name}'...",
                    rgb_sys=False,
                    ready_color="blue"
                )
            )

            if not manager.has_screen(screen_name):
                raise BigManager.Errors(f"Screen with name '{screen_name}' was not found.")

            self.current = manager_name
            manager.current = screen_name

            print(
                Color(
                    text=f"[{self.name}][{manager_name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Screen with name '{screen_name}' was found and set successfully.",
                    rgb_sys=False,
                    ready_color="green"
                )
            )
            return

        else:
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"No manager name entered.",
                    rgb_sys=False,
                    ready_color="red"
                ),
                Color(
                    text=f"Finding screen with name '{screen_name}'...",
                    rgb_sys=False,
                    ready_color="blue"
                )
            )

            if screen_name not in self._screens_:
                raise BigManager.Errors(f"Screen with name '{screen_name}' was not found.")

            self.current = screen_name

            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Screen with name '{screen_name}' was found and set successfully.",
                    rgb_sys=False,
                    ready_color="green"
                )
            )
            return

    def create_file(self, path: str, parent_count: int = 0):
        create_file(path, parent_count)

    def get_data_others_data(self):
        if self.manager is None:
            raise BigManager.Errors("No manager was found.")
        return self.manager.get_data(self.name)

    def get_data(self, **dir_get):
        if not dir_get:
            return self.data.get_all()
        data_key = dir_get.get("data_key", "")
        if not isinstance(data_key, str):
            raise TypeError("Data key must be a string.")
        data_key = data_key.strip()
        if not data_key:
            raise ValueError("Data key can't be empty.")
        as_file = dir_get.get("as_file", None)
        if as_file is None:
            raise ValueError("'as_file' must be set.")
        if not isinstance(as_file, bool):
            raise TypeError("'as_file' must be a boolean.")
        del dir_get["data_key"], dir_get["as_file"]
        return self.data.get(
            data_key= data_key,
            as_file= as_file,
            kwargs= dir_get
        )

class ConnectionManager(ScreenManager):
    class Errors(Exception):
        pass

    def __init__(self, name: str, **kwargs):
        if not isinstance(name, str):
            raise TypeError("Name must be a string.")
        name = name.strip()
        if not name:
            raise ValueError("ConnectionManager name can't be empty.")
        super().__init__(**kwargs)
        self.name = name
        self.connect_able = True
        self.utils_path = Path(__file__).parent / "BigManager`s util.json"
        with open(self.utils_path, "r") as file:
            utils = json.load(file)

        if "ConnectionManagers exist" not in utils.keys():
            utils["ConnectionManagers exist"] = 1
        else:
            utils["ConnectionManagers exist"] += 1
        if "ConnectionManagers ids" not in utils.keys():
            utils["ConnectionManagers ids"] = []

        def gen_id():
            id = "ConnectionManager_"
            for i in range(5):
                symb = random.choice([
                    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                    "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                    "u", "v", "w", "x", "y", "z"
                ])
                caps = random.choice([True, False])
                _int = random.choice([True, False])
                if caps:
                    symb = symb.upper()
                if _int:
                    symb = str(random.randint(0, 9))
                id += symb
            return id

        self.id = gen_id()

        while self.id in utils["ConnectionManagers ids"]:
            self.id = gen_id()

        utils["ConnectionManagers ids"].append(self.id)
        with open(self.utils_path, "w") as file:
            json.dump(utils, file)
        self.managers = []

    # baned screenmanager funcs
    def add_widget(self, widget, *args, **kwargs):
        raise ConnectionManager.Errors("This func is not allowed.")

    def remove_widget(self, widget, *args, **kwargs):
        raise ConnectionManager.Errors("This func is not allowed.")

    # ConnectionManager funcs
    def connect(self, bigmanager1: BigManager, bigmanager2: BigManager):
        if not self.connect_able:
            raise ConnectionManager.Errors("ConnectionManager is full.(max 1 connection)")

        if not isinstance(bigmanager1, BigManager) or not isinstance(bigmanager2, BigManager):
            raise TypeError("You can connect BigManagers only.")

        if bigmanager1 is bigmanager2:
            raise ConnectionManager.Errors("You can't connect BigManager to itself.")

        if bigmanager1.name == bigmanager2.name:
            raise ConnectionManager.Errors("BigManagers must have different names.")

        if not bigmanager1.name.strip() or not bigmanager2.name.strip():
            raise ConnectionManager.Errors("BigManager names can't be empty.")

        if bigmanager1.manager is not None or bigmanager2.manager is not None:
            raise ConnectionManager.Errors("One or both BigManagers are already connected.")

        if hasattr(self, bigmanager1.name) or hasattr(self, bigmanager2.name):
            raise ConnectionManager.Errors("One or both BigManager names are unconnectable.")

        print(
            Color(text=f"[{self.name}]", rgb_sys=False, ready_color="purple"),
            Color(
                text=f"Connecting bigmanager '{bigmanager1.name}' with bigmanager '{bigmanager2.name}'...",
                rgb_sys=False,
                ready_color="blue"
            )
        )

        try:
            bigmanager1.connect(self)

            bigmanager2.connect(self)

            screen1 = Screen(name=bigmanager1.name)
            screen1.inner_manager = bigmanager1
            screen1.add_widget(bigmanager1)

            screen2 = Screen(name=bigmanager2.name)
            screen2.inner_manager = bigmanager2
            screen2.add_widget(bigmanager2)

            super().add_widget(screen1)
            super().add_widget(screen2)

            setattr(self, bigmanager1.name, screen1)
            setattr(self, bigmanager2.name, screen2)

            self.managers.extend([bigmanager1.name, bigmanager2.name])
            self.connect_able = False

        except Exception:
            if bigmanager2.manager is self:
                bigmanager2.disconnect()

            if bigmanager1.manager is self:
                bigmanager1.disconnect()

            for screen in self.screens[:]:
                super().remove_widget(screen)

            for manager_name in (bigmanager1.name, bigmanager2.name):
                if hasattr(self, manager_name):
                    delattr(self, manager_name)

            self.managers.clear()
            self.connect_able = True
            raise

        print(
            Color(text=f"[{self.name}]", rgb_sys=False, ready_color="purple"),
            Color(text="Connected successfully.", rgb_sys=False, ready_color="green")
        )

    def disconnect(self):
        if self.connect_able:
            raise ConnectionManager.Errors("No BigManagers connected.")

        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text="Disconnecting the BigManagers...",
                rgb_sys=False,
                ready_color="blue"
            )
        )

        for manager_name in self.managers[:]:
            screen = getattr(self, manager_name)
            bigmanager = screen.inner_manager

            super().remove_widget(screen)
            bigmanager.disconnect()

            delattr(self, manager_name)

            print(
                Color(
                    text=f"[{self.name}][{manager_name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text="Disconnected successfully.",
                    rgb_sys=False,
                    ready_color="green"
                )
            )

        self.managers.clear()
        self.connect_able = True

        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text="BigManagers were disconnected.",
                rgb_sys=False,
                ready_color="green"
            )
        )

    def set_current_screen(self, screen_name: str, got_from: str, manager_name: str = ""):
        if not isinstance(screen_name, str):
            raise ConnectionManager.Errors("Screen name must be 'str'.")
        if not isinstance(got_from, str):
            raise ConnectionManager.Errors("'got_from' must be 'str'.")
        if not isinstance(manager_name, str):
            raise ConnectionManager.Errors("Manager name must be 'str'.")

        screen_name = screen_name.strip()
        manager_name = manager_name.strip()
        got_from = got_from.strip()

        if got_from == "":
            raise ConnectionManager.Errors("'got_from' must be set.")
        if not hasattr(self, got_from) or got_from not in self.managers:
            raise ConnectionManager.Errors("Unknown BigManager")
        if got_from == self.managers[1]:
            bigmanager = getattr(self, self.managers[0]).inner_manager
        else:
            bigmanager = getattr(self, self.managers[1]).inner_manager
        self.current = bigmanager.name
        print(
            Color(
                text=f"[{got_from}][{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Successfully switched to BigManager '{bigmanager.name}'.",
                rgb_sys=False,
                ready_color="green"
            )
        )
        bigmanager.set_current_screen(
            screen_name=screen_name,
            manager_name=manager_name,
            own=True
        )

    def get_data(self, got_from: str, **kwargs):
        if not hasattr(self, got_from) or got_from not in self.managers:
            raise ConnectionManager.Errors("Unknown BigManager name.")
        if got_from == self.managers[1]:
            manager = getattr(self, self.managers[0]).inner_manager
        else:
            manager = getattr(self, self.managers[1]).inner_manager

        if kwargs:
            return manager.get_data(kwargs)
        return manager.get_data()

class DataManager:
    class Errors(Exception):
        pass
    def __init__(self, name: str, workspace_path: str = ""):
        if not isinstance(name, str):
            raise DataManager.Errors("Name must be 'str'.")
        name = name.strip()
        if not name:
            raise DataManager.Errors("'name' must be set.")
        if not isinstance(workspace_path, str):
            raise DataManager.Errors("'workspace_path' must be 'str'.")
        self.workspace = ""
        if workspace_path:
            create_folder(workspace_path)
            self.workspace = workspace_path
        self.data = {}
        self.saved_in_file = []
        self.name = name
    def set_workspace(self, path: str):
        if not isinstance(path, str):
            raise DataManager.Errors("'path' must be 'str'.")
        path = path.strip()
        if not path:
            raise DataManager.Errors("'path' must be set.")
        create_folder(path)
        self.workspace = path
        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Workspace '{path}' was set.",
                rgb_sys=False,
                ready_color="green"
            )
        )
    def remove_workspace(self):
        self.workspace = ""
        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Workspace removed.",
                rgb_sys=False,
                ready_color="green"
            )
        )
    def add(self, data_key: str, data, as_file = "False/True/both", **kwargs):
        if not isinstance(data_key, str):
            raise DataManager.Errors("'data_key' must be 'str'.")
        path = kwargs.get("path", "")
        if not isinstance(path, str):
            raise DataManager.Errors("'path' must be 'str'.")
        if str(as_file).strip() == "False/True/both":
            as_file = False
        path = path.strip()
        if isinstance(as_file, str):
            if (as_file := as_file.strip().lower()) != "both":
                raise DataManager.Errors("'as_file' must be 'bool' or str('both').")
        elif not isinstance(as_file, bool):
            raise DataManager.Errors("'as_file' must be 'bool' or str('both').")

        if as_file:
            if not self.workspace:
                raise DataManager.Errors("'workspace_path' not set.")
            file_name = kwargs.get("file_name", "")
            if not isinstance(file_name, str):
                raise DataManager.Errors("'file_name' must be 'str'.")
            file_name = file_name.strip()
            if not file_name:
                raise DataManager.Errors("'file_name' must be set.")
            if not file_name.lower().endswith(".json"):
                raise DataManager.Errors("'file_name' must be a 'json' file.")
            file_path = kwargs.get("file_path", "")
            if not isinstance(file_path, str):
                raise DataManager.Errors("'file_path' must be 'str'.")
            full_path = f"{self.workspace}/"
            if file_path:
                full_path += f"{file_path}/"
            full_path += file_name
            create_json_file(full_path)
            with open(full_path, "r") as f:
                file = json.load(f)
            file[data_key] = data
            with open(full_path, "w") as f:
                json.dump(file, f)
            self.saved_in_file.append(full_path)
            if as_file != "both":
                return
        value = self.data
        completed_path = f"[{self.name}][PRIVATE DATA]"
        if path:
            split_obj = kwargs.get("split", ".")
            if not isinstance(split_obj, str):
                raise DataManager.Errors("'split_obj' must be 'str'.")
            split_obj = split_obj.strip()
            if not split_obj:
                raise DataManager.Errors("'split_obj' must be set.")
            path = path.split(split_obj)
            for item in path:
                if item not in value:
                    value[item] = {}
                    print(
                        Color(
                            text=completed_path,
                            rgb_sys=False,
                            ready_color="purple"
                        ),
                        Color(
                            text=f"Created item '{item}'.",
                            rgb_sys=False,
                            ready_color="blue"
                        )
                    )
                if not isinstance(value[item], dict):
                    print(
                        Color(
                            text=f"[{self.name}][ADD]{completed_path}[{item}]",
                            rgb_sys=False,
                            ready_color="purple"
                        ),
                        Color(
                            text=f"Adding stopped because value of key '{item}' isn`t a 'dict'.",
                            rgb_sys=False,
                            ready_color="red"
                        )
                    )
                    return
                value = value[item]
                completed_path += f"[{item}]"
        value[data_key] = data
        print(
            Color(
                text=completed_path,
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Data under key '{data_key}' was added successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )
    def delete(self, data_key: str, as_file: bool = False, **kwargs):
        if self.workspace and is_folder_empty(self.workspace) and not self.data:
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"No data saved yet.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return

        if not isinstance(data_key, str):
            raise DataManager.Errors("'data_key' must be 'str'.")
        if not isinstance(as_file, bool):
            raise DataManager.Errors("'as_file' must be 'bool'.")
        value = self.data
        completed_path = f"[{self.name}][PRIVATE DATA]"
        route = ""
        if as_file:
            if not self.workspace:
                raise DataManager.Errors("'workspace_path' not set.")
            route = kwargs.get("route", "")
            if not isinstance(route, str):
                raise DataManager.Errors("'route' must be 'str'.")
            file_name = str(kwargs.get("file_name", "")).strip()
            if not file_name:
                raise DataManager.Errors("'file_name' must be set.")
            if not file_name.lower().endswith(".json"):
                raise DataManager.Errors("'file_name' must be a 'json' file.")
            route = route.strip()
            _route_ = route
            route_ = f"{self.workspace}/"
            if route:
                route_ += f"{route}/"
            route = route_
            del route_
            route += f"{file_name}"
            if not can_access_file(route):
                raise FileNotFoundError(f"Cannot access JSON file: {route}")
            with open(route, "r") as f:
                file = json.load(f)
            completed_path = f"[{self.name}][WORKSPACE][{_route_}/{file_name}][{Color(text='DELETE', rgb_sys=False, ready_color="red")}]"
            value = file
        path = kwargs.get("path", "")
        if not isinstance(path, str):
            raise DataManager.Errors("'path' must be 'str'.")
        path = path.strip()
        if path:
            split_obj = kwargs.get("split", ".")
            if not isinstance(split_obj, str):
                raise DataManager.Errors("'split_obj' must be 'str'.")
            split_obj = split_obj.strip()
            if not split_obj:
                raise DataManager.Errors("'split_obj' must be set.")
            path = path.split(split_obj)
            for item in path:
                if not isinstance(value, dict):
                    print(
                        Color(
                            text=completed_path,
                            rgb_sys=False,
                            ready_color="purple"
                        ),
                        Color(
                            text=f"Value is not a 'dict'.",
                            rgb_sys=False,
                            ready_color="red"
                        )
                    )
                    return

                if item not in value:
                    print(
                        Color(
                            text=completed_path,
                            rgb_sys=False,
                            ready_color="purple"
                        ),
                        Color(
                            text=f"Could not find item '{item}'.",
                            rgb_sys=False,
                            ready_color="red"
                        )
                    )
                    return
                value = value[item]
                completed_path += f"[{item}]"
        if not isinstance(value, dict):
            raise DataManager.Errors("Target value must be a 'dict'.")
        if data_key not in value:
            print(
                Color(
                    text=completed_path,
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Data with key '{data_key}' was not found.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return
        del value[data_key]
        if as_file:
            with open(route, "w") as f:
                json.dump(file, f)
        print(
            Color(
                text=completed_path,
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Data under key '{data_key}' was deleted successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )
    def get(self, data_key: str, as_file: bool = False, **kwargs):
        if self.workspace and is_folder_empty(self.workspace) and not self.data:
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"No data saved yet.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return None, "No data saved yet."

        if not isinstance(data_key, str):
            raise DataManager.Errors("'data_key' must be 'str'.")
        if not isinstance(as_file, bool):
            raise DataManager.Errors("'as_file' must be 'bool'.")
        value = self.data
        completed_path = f"[{self.name}][PRIVATE DATA]"
        if as_file:
            if not self.workspace:
                raise DataManager.Errors("'workspace_path' not set.")
            route = kwargs.get("route", "")
            if not isinstance(route, str):
                raise DataManager.Errors("'route' must be 'str'.")
            file_name = str(kwargs.get("file_name", "")).strip()
            if not file_name:
                raise DataManager.Errors("'file_name' must be set.")
            if not file_name.lower().endswith(".json"):
                raise DataManager.Errors("'file_name' must be a 'json' file.")
            route = route.strip()
            route_ = f"{self.workspace}/"
            if route:
                route_ += f"{route}/"
            route = route_
            del route_
            route += f"{file_name}"
            if not can_access_file(route):
                raise FileNotFoundError(f"Cannot access JSON file: {route}")
            with open(route, "r") as f:
                file = json.load(f)
            if data_key not in file:
                print(
                    Color(
                        text=f"[{self.name}][WORKSPACE][{route}]",
                        rgb_sys=False,
                        ready_color="purple"
                    ),
                    Color(
                        text=f"No item with key '{data_key}' was found.",
                        rgb_sys=False,
                        ready_color="red"
                    )
                )
                return None, f"File does not have key '{data_key}'."
            completed_path = f"[{self.name}][WORKSPACE][{route}][{Color(text='GET', rgb_sys=False, ready_color="blue")}]"
            value = file
        path = kwargs.get("path", "")
        if not isinstance(path, str):
            raise DataManager.Errors("'path' must be 'str'.")
        path = path.strip()
        if path:
            split_obj = kwargs.get("split", ".")
            if not isinstance(split_obj, str):
                raise DataManager.Errors("'split_obj' must be 'str'.")
            path = path.split(split_obj)
            for item in path:
                if not isinstance(value, dict):
                    return None, f"'{value}' is not a dictionary."
                if item not in value:
                    print(
                        Color(
                            text=completed_path,
                            rgb_sys=False,
                            ready_color="purple"
                        ),
                        Color(
                            text=f"Could not find item '{item}'.",
                            rgb_sys=False,
                            ready_color="red"
                        )
                    )
                    return None, f"Item '{item}' not found."
                value = value[item]
                completed_path += f"[{item}]"
        if not isinstance(value, dict):
            return None, f"'{value}' is not a dictionary."
        if data_key not in value:
            print(
                Color(
                    text=completed_path,
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"Data with key '{data_key}' was not found.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return None, f"Data with key '{data_key}' not found."

        print(
            Color(
                text=completed_path,
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Data under key '{data_key}' was got successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )
        return value[data_key], "Got successfully."
    def get_all(self):
        if self.workspace and is_folder_empty(self.workspace) and not self.data:
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"No data saved yet.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return None
        return_data = copy.deepcopy(self.data)
        if self.saved_in_file:
            for route in self.saved_in_file:
                with open(route, "r") as f:
                    _route_ = json.load(f)
                return_data[route] = _route_
        print(
            Color(
                text="Returning:",
                rgb_sys=False,
                ready_color="purple"
            )
        )
        for k,i in return_data.items():
            print(
                Color(
                    text=f"{k}: {i}",
                    rgb_sys=False,
                    ready_color="blue"
                )
            )
        print(
            Color(
                text= "-",
                rgb_sys=False,
                ready_color="purple"
            )*30
        )
        return return_data
    def clear(self, **kwargs):
        if self.workspace and is_folder_empty(self.workspace) and not self.data:
            print(
                Color(
                    text=f"[{self.name}]",
                    rgb_sys=False,
                    ready_color="purple"
                ),
                Color(
                    text=f"No data saved yet.",
                    rgb_sys=False,
                    ready_color="red"
                )
            )
            return

        ignore_keys = kwargs.get("ignore_keys", {})
        folder_keys = []
        data_keys = []
        if not isinstance(ignore_keys, dict):
            raise DataManager.Errors("'ignore_keys' must be 'dict'.")
        if ignore_keys:
            if not set(ignore_keys).issubset({"folder_keys", "data_keys"}):
                raise DataManager.Errors("'ignore_keys' must have 'folder_keys' and 'data_keys' only.")

            data_keys = ignore_keys.get("data_keys", [])
            if not isinstance(data_keys, list):
                raise DataManager.Errors("'data_keys' must be 'list'.")
            folder_keys = ignore_keys.get("folder_keys", [])
            if not isinstance(folder_keys, list):
                raise DataManager.Errors("'folder_keys' must be 'list'.")

        for route in self.saved_in_file.copy():
            will_delete = True

            for k in folder_keys:
                if k in route.split("/"):
                    will_delete = False
                    break

            if will_delete:
                remove_file(route)
                self.saved_in_file.remove(route)

        def clear_dict(dictionary: dict) -> None:
            for key, value in list(dictionary.items()):
                if key in data_keys:
                    continue

                if isinstance(value, dict):
                    clear_dict(value)

                    if not value:
                        del dictionary[key]
                else:
                    del dictionary[key]

        clear_dict(self.data)

        print(
            Color(
                text=f"[{self.name}]",
                rgb_sys=False,
                ready_color="purple"
            ),
            Color(
                text=f"Data was cleared successfully.",
                rgb_sys=False,
                ready_color="green"
            )
        )