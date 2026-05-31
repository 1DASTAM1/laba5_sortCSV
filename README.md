Создание csv файла и его сортировка по разным ключам, в файле генерируется что то типо статистики игроков в футболе на каком то матче.
Окно и генератор написанны на Python, а варианты сортировки на C++ и Python. Сортировка на C++ компилируется в dll и с помощью ctypes используется в Python.

Комманда в vs code для создания dll в Circular_Queue1.cpp (для MinGW gcc/cpp): 
g++.exe -shared -static -static-libgcc -static-libstdc++ -o sortCPP.dll sortCPP.cpp
