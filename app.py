from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton,
    QLabel, QTableView, QLineEdit, QMessageBox, QHBoxLayout
)
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from db_manager import initialize_database


class TreeClicker(QMainWindow):
    def __init__(self):
        super().__init__()

        
        self.db = initialize_database()

        
        self.model = QSqlTableModel()
        self.model.setTable("gardener")
        self.model.setEditStrategy(QSqlTableModel.OnFieldChange)  
        self.model.select()

        self.setWindowTitle("Tree Clicker with QSqlTableModel")
        self.setGeometry(100, 100, 800, 500)

       
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

       
        self.layout = QVBoxLayout(self.central_widget)

        
        self.table_view = QTableView()
        self.table_view.setModel(self.model)
        self.table_view.resizeColumnsToContents()
        self.layout.addWidget(self.table_view)

        
        self.input_layout = QHBoxLayout()
        self.name_input = QLineEdit(self, placeholderText="Имя садовника")
        self.salary_input = QLineEdit(self, placeholderText="Зарплата")
        self.input_layout.addWidget(self.name_input)
        self.input_layout.addWidget(self.salary_input)
        self.layout.addLayout(self.input_layout)

        
        self.button_layout = QHBoxLayout()

        self.add_button = QPushButton("Добавить")
        self.add_button.clicked.connect(self.add_gardener)
        self.button_layout.addWidget(self.add_button)

        self.delete_button = QPushButton("Удалить выбранного")
        self.delete_button.clicked.connect(self.delete_gardener)
        self.button_layout.addWidget(self.delete_button)

        self.layout.addLayout(self.button_layout)

    def add_gardener(self):
        """Добавление нового садовника в базу данных."""
        name = self.name_input.text().strip()
        salary = self.salary_input.text().strip()

        if not name or not salary.isdigit():
            QMessageBox.warning(self, "Ошибка", "Введите корректные данные.")
            return

       
        row = self.model.rowCount()
        self.model.insertRow(row)
        self.model.setData(self.model.index(row, 1), name)
        self.model.setData(self.model.index(row, 2), int(salary))

        if self.model.submitAll():
            self.name_input.clear()
            self.salary_input.clear()
        else:
            QMessageBox.critical(self, "Ошибка", "Не удалось добавить запись.")

    def delete_gardener(self):
        """Удаление выбранной записи."""
        index = self.table_view.currentIndex()
        if not index.isValid():
            QMessageBox.warning(self, "Ошибка", "Выберите запись для удаления.")
            return

        self.model.removeRow(index.row())
        if not self.model.submitAll():
            QMessageBox.critical(self, "Ошибка", "Не удалось удалить запись.")


if __name__ == "__main__":
    app = QApplication([])
    window = TreeClicker()
    window.show()
    app.exec()
