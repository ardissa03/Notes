from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import json

shenimet = {
    'Welcome':{
        "text": "This is the best note taking app",
        "tags": ["good","instructions"]
    }    
}

with open("notes.json","w") as file:
    json.dump(shenimet,file)


app = QApplication([])
notes_win = QWidget()
notes_win.setWindowTitle("Smart Notes")
notes_win.resize(900,600)

list_notes = QListWidget()
list_notes_label = QLabel("List of notes")

create_button = QPushButton("Create note")
delete_note = QPushButton("Delete note")
save_note_button = QPushButton("Save note")

list_tags = QListWidget()
list_tags_label = QLabel ("List of tags")
field_tag = QLineEdit("")
field_tag.setPlaceholderText("Enter tag...")

add_button = QPushButton("Add to note")
del_tag_button = QPushButton("Untag from note")
search_button = QPushButton("Search notes by tag")

field_text = QTextEdit()

layot_notes = QHBoxLayout()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_1.addWidget(create_button)
row_1.addWidget(delete_note)


row_2 = QHBoxLayout()
row_2.addWidget(save_note_button)
col_2.addLayout(row_1)
col_2.addLayout(row_2)

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(add_button)
row_3.addWidget(del_tag_button)

row_4 = QHBoxLayout()
row_4.addWidget(search_button)

col_2.addLayout(row_3)
col_2.addLayout(row_4)

layot_notes.addLayout(col_1,stretch=2)
layot_notes.addLayout(col_2,stretch=2)

notes_win.setLayout(layot_notes)

def add_note():
    note_name,ok = QInputDialog.getText(notes_win,"Add note","Note name:")

    if ok and note_name!="":
        shenimet[note_name]={"text":"","tags":[]}
        list_notes.addItem(note_name)
        list_tags.addItems(shenimet[note_name]["tags"])
        print(shenimet)

def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        shenimet[key]["text"]= field_text.toPlainText()

        with open("notes.json") as file:
            json.dump(shenimet,file,sort_keys=True,ensure_ascii=False)
        print(shenimet)
    else:
        print("Note to save is not selected!")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del shenimet[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(shenimet)
        with open("notes.json","w") as  file:
            json.dump(shenimet,file,sort_keys=True,ensure_ascii=False)
        print(shenimet)
    else:
        print("Note to be deleted is not selected!")
        
def show_note():
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(shenimet[key]["text"])
    list_tags.clear()
    list_tags.addItems(shenimet[key]["tags"])

def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()

        if not tag in shenimet[key]["tags"]:
            shenimet[key]["tags"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes.json","w") as file:
            json.dump(shenimet,file,sort_keys=True,ensure_ascii=False)
        print(shenimet)
    else:
        print("Note to add a tag is not selected!")

def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()

        shenimet[key]["tags"].remove(tag)
        list_tags.clear()
        list_tags.addItems(shenimet[key]["tags"])
        with open("notes.json","w") as file:
            json.dump(shenimet,file,sort_keys=True,ensure_ascii=False)
        print(shenimet)
    else:
        print("Tag to delete is not selected!")

def search_tag():
    print(search_button.text())
    tag = field_tag.text()
    if search_button.text()=="Search notes by tag" and tag:
        print(tag)
        notes_filtered = {}    
        for note in shenimet:
            if tag in shenimet[note]["tags"]:
                notes_filtered[note]=shenimet[note]   
        search_button.setText("Reset search") 
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(search_button.text())       

    elif search_button == "Reset search":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(shenimet)
        search_button.setText("Search notes by tag")
        print(search_button.text())
    else:
        pass


add_button.clicked.connect(add_note)
list_notes.itemClicked.connect(show_note)
save_note_button.clicked.connect(save_note)
delete_note.clicked.connect(del_note)
add_button.clicked.connect(add_tag)
del_tag_button.clicked.connect(del_tag)
search_button.clicked.connect(search_tag)

notes_win.show()
with open("notes.json","r") as file:
    shenimet = json.load(file)
list_notes.addItems(shenimet)

app.exec_()



