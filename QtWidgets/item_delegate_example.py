import sys
from PyQt4 import QtCore, QtGui


class DelegatedExample(QtGui.QItemDelegate):

    def __init__(self, owner, labels):
        QtGui.QItemDelegate.__init__(self, owner)
        self.table = owner
        self.color = QtGui.QColor('red')
        self.labels = labels
        self.button_1_text = 'my button 1'
        self.button_2_text = 'my button 2'
        self.button_3_text = 'my button 3'

    def paint(self, painter, option, index):
        row, column = index.row(), index.column()
        style = QtGui.QApplication.style()
        if column == 0:
            painter.setPen(QtGui.QPen())
            painter.setBrush(QtGui.QBrush(self.color))
            painter.drawRect(QtCore.QRect(
                option.rect.left() + 5,
                option.rect.top() + 5,
                option.rect.width() - 15,
                option.rect.height() - 10))
            return

        elif column == 1:
            opt = QtGui.QStyleOptionButton()
            opt.rect = option.rect
            style.drawControl(QtGui.QStyle.CE_CheckBox, opt, painter)
            return

        elif column == 2:
            # fill style options with item data
            opt = QtGui.QStyleOptionViewItemV4()
            # draw item data as CheckBox
            self.drawDisplay(painter, option, option.rect, self.labels[row])
            return

        elif column in (3, 4, 5):
            opt = QtGui.QStyleOptionButton()
            opt.text = (
                self.button_1_text,
                self.button_2_text,
                self.button_3_text)[column - 3]
            opt.textVisible = True
            opt.rect = option.rect

            # draw item data as CheckBox
            style.drawControl(QtGui.QStyle.CE_PushButton, opt, painter)
            return

        QtGui.QItemDelegate.paint(self, painter, option, index)

    def createEditor(self, parent, option, index):
        row, column = index.row(), index.column()
        if column == 1:
            editor = QtGui.QCheckBox(parent)
            return editor

        elif column == 2:
            editor = QtGui.QLineEdit(self.labels[row], parent)
            return editor

        elif column == 3:
            editor = QtGui.QPushButton(self.button_1_text, parent)
            return editor

        elif column == 4:
            editor = QtGui.QPushButton(self.button_2_text, parent)
            return editor

        elif column == 5:
            editor = QtGui.QPushButton(self.button_3_text, parent)
            return editor

        return QtGui.QAbstractItemDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        row, column = index.row(), index.column()

        if column == 2:
            self.labels[index.row()] = editor.text()
            return

        elif column == 3:
            print(self.button_1_text + ' is clicked, row ' + str(row))
            return

        elif column == 4:
            print(self.button_2_text + ' is clicked, row ' + str(row))
            return

        elif column == 5:
            print(self.button_3_text + ' is clicked, row ' + str(row))
            return

        QtGui.QAbstractItemDelegate.setEditorData(self, editor, index)

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)

    def sizeHint(self, option, index):
        col = index.column()
        if col <= 1:
            return QtCore.QSize(10, 10)
        elif col == 2:
            return QtCore.QSize(200, 10)
        else:
            return QtCore.QSize(125, 20)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    tableView = QtGui.QTableView()
    tableView.setShowGrid(False)
    tableView.setAlternatingRowColors(True)
    tableView.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
    tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    tableView.setFocusPolicy(QtCore.Qt.NoFocus)
    tableView.horizontalHeader().setResizeMode(
        QtGui.QHeaderView.ResizeToContents)

    tableView.horizontalHeader().hide()
    tableView.verticalHeader().hide()

    labels = ['my text', 'my text', 'taratata', 'turlututu']

    model = QtGui.QStandardItemModel(len(labels), 6)
    tableView.setModel(model)
    tableView.setEditTriggers(QtGui.QAbstractItemView.AllEditTriggers)
    tableView.viewport().installEventFilter(tableView)

    delegate = DelegatedExample(tableView, labels)
    tableView.setItemDelegate(delegate)

    tableView.setWindowTitle("Items Delegate")
    tableView.show()
    sys.exit(app.exec_())
