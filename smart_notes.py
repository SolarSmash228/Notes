from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
import json

app = QApplication([])

layout = QVBoxLayout()
layout1 = QVBoxLayout()
layout2 = QHBoxLayout()
layout3 = QHBoxLayout()
layout4 = QHBoxLayout()

notes = {
    'Название заметки':
        {
        'текст':'текст заметки',
        'теги':['черновик']
        }
}
with open('notes_data.json', 'w', encoding='utf-8') as file:
    json.dump(notes, file, ensure_ascii=False)

btn1 = QPushButton('Искать заметку по тегу')
btn2 = QPushButton('Открепить от заметки')
btn3 = QPushButton('Добавить к заметке')
btn4 = QPushButton('Сохранить заметку')
btn5 = QPushButton('Удалить заметку')
btn6 = QPushButton('Создать заметку')
te1 = QTextEdit()
lw1 = QListWidget()
lw2 = QListWidget()
le1 = QLineEdit()
lab1 = QLabel('Список заметок')
lab2 = QLabel('Список тегов')
le1.setPlaceholderText('Введите тег...')

layout.addWidget(te1)
layout1.addWidget(lab1)
layout1.addWidget(lw1)
layout3.addWidget(btn6)
layout3.addWidget(btn5)
layout1.addLayout(layout3)
layout1.addWidget(btn4)
layout1.addWidget(lab2)
layout1.addWidget(lw2)
layout1.addWidget(le1)
layout1.addWidget(btn3)
layout4.addWidget(btn2)
layout1.addLayout(layout4)
layout1.addWidget(btn1)

layout2.addLayout(layout)
layout2.addLayout(layout1)

def show_note():
    name = lw1.selectedItems()[0].text()
    te1.setText(notes[name]['текст'])
    lw2.clear()
    lw2.addItems(notes[name]['теги'])

def add_note():
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки:')
    if ok and note_name != '':
        notes[note_name] = {'текст' : '', 'теги' : []}
        lw1.addItem(note_name)

def del_note():
    if lw1.selectedItems():
        key = lw1.selectedItems()[0].text()
        del notes[key]
        lw1.clear()
        lw2.clear()
        te1.clear()
        with open ('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii=False)

def save_note():
    if lw1.selectedItems():
        key = lw1.selectedItems()[0].text()
        notes[key]['текст'] = te1.toPlainText()
        with open ('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii=False)

def del_tag():
    if lw2.selectedItems():
        key = lw1.selectedItems()[0].text()
        tag = lw2.selectedItems()[0].text()
        notes[key]['теги'].remove(tag)
        lw2.clear()
        lw2.addItems(notes[key]['теги'])
        with open ('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii=False)

def add_tag():
    if lw1.selectedItems():
        key = lw1.selectedItems()[0].text()
        tag = le1.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            lw2.addItem(tag)
            le1.clear()
        with open ('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(notes, file, sort_keys = True, ensure_ascii=False)
    else:
        print('Заметка для добавления тега не выбрана')



def search_tag():
    tag = le1.text()
    if button_tag_search.text() == 'Искать заметку по тегу':
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]['теги']:
                notes_filtered[note]=notes[note]
        button_tag_search.setText('Сбросить поиск')
        lw1.clear()
        lw2.clear()
        lw1.addItems(notes_filtered)
    elif button_tag_search.text() == 'Сбросить поиск':
        le1.clear()
        lw1.clear()
        lw2.clear()
        lw1.addItems(notes)
        button_tag_search.setText('Искать заметки по тегу')
    else:
        pass

btn6.clicked.connect(add_note)
btn5.clicked.connect(del_note)
btn4.clicked.connect(save_note)
btn3.clicked.connect(add_tag)
btn2.clicked.connect(del_tag)
btn1.clicked.connect(search_tag)
lw1.itemClicked.connect(show_note)
window = QWidget()
window.setLayout(layout2)
window.setWindowTitle('Умные заметки')
window.resize(400,200)
window.show()
with open ('notes_data.json', 'r', encoding='utf-8') as file:
    notes = json.load(file)
lw1.addItems(notes)
app.exec()
