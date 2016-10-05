from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys


class Editor(QMainWindow):
    
    def __init__(self, parent=None, scale=1):
        QMainWindow.__init__(self, parent)
        self.initFileInfo()
        self.initUI(scale)
    
    def initFileInfo(self):
        self.file_name = ''
        
    def initUI(self, scale):
        self.getScreenSize()
        
        self.initMainTextBox()        
        self.initToolBar()
        self.initFormatBar()
        self.initMenuBar()
        self.statusbar = self.statusBar()
        
        self.setMinimumSize(QSize(self.win_width * scale, self.win_height * scale))
        self.setWindowTitle('Text Editor')
        
    def initMainTextBox(self):
        self.main_txt_box = QTextEdit(self)
        self.main_txt_box.setTabStopWidth(30)
        self.main_txt_box.setDocumentTitle('UntitledDoc')
        self.main_txt_box.setFontPointSize(12)
        self.main_txt_box.cursorPositionChanged.connect(self.cursorPosition)
        self.setCentralWidget(self.main_txt_box)
        
    def getScreenSize(self):
        self.win_width = QApplication.desktop().screenGeometry().width()
        self.win_height = QApplication.desktop().screenGeometry().height()
        
    def initMenuBar(self):
        menubar = self.menuBar()
        entries = ['File', 'Edit', 'Tools', 'View']
        entries_var = {}
        for entry in entries:
            entries_var[entry] = menubar.addMenu(entry)
        entries_var['File'].addAction(self.actions['New'])
        entries_var['File'].addAction(self.actions['Open'])
        entries_var['File'].addAction(self.actions['Save'])
        entries_var['File'].addAction(self.actions['Print'])
        entries_var['File'].addAction(self.actions['Preview'])
        entries_var['Edit'].addAction(self.actions['Cut'])
        entries_var['Edit'].addAction(self.actions['Copy'])
        entries_var['Edit'].addAction(self.actions['Paste'])
        entries_var['Edit'].addAction(self.actions['Undo'])
        entries_var['Edit'].addAction(self.actions['Redo'])
        action_name = ['Toggle Toolbar','Toggle Formatbar','Toggle Statusbar']
        action_handler_fcn = {'Toggle Toolbar' : self.toggleToolbar,'Toggle Formatbar' : self.toggleFormatbar,'Toggle Statusbar' : self.toggleStatusbar}
        for i in range(len(action_name)):
            temp_actn = QAction(action_name[i], self)
            temp_actn.triggered.connect(action_handler_fcn[action_name[i]])
            entries_var['View'].addAction(temp_actn)
        
    def initToolBar(self):
        action_name = ['New', 'Open', 'Save', 'Print', 'Preview', 'Cut', 'Copy', 'Paste', 'Undo', 'Redo', 'Insert bullet list', 'Insert numbered list']
        action_status_tip = ['Create new document.', 'Open existing document.', 'Save open document.', 'Print document.', 'Preview for printing.', 'Cut text to clipboard', 'Copy text to clipboard',
                             'Paste text to document', 'Undo last action', 'Redo last action', 'Insert bullet list', 'Insert numbered list']
        action_shortcut = ['Ctrl+N', 'Ctrl+O', 'Ctrl+S', 'Ctrl-P', 'Ctrl+Shift+P', 'Ctrl-X', 'Ctrl-C', 'Ctrl-V', 'Ctrl-Z', 'Ctrl-Y', 'Ctrl+Shift+B', 'Ctrl+Shift+L']
        action_handler_fcn = {'New': self.new_doc, 'Open': self.open_doc, 'Save': self.save_doc, 'Print': self.print_, 'Preview': self.preview, 'Cut': self.main_txt_box.cut, 'Copy': self.main_txt_box.copy, 'Paste': self.main_txt_box.paste, 'Undo': self.main_txt_box.undo,
                              'Redo': self.main_txt_box.redo, 'Insert bullet list': self.bulletList, 'Insert numbered list': self.numberedList}
        self.toolbar = self.addToolBar('Options')
        # action inits
        self.actions = {}
        for i in range(len(action_name)):
            temp_actn = QAction(action_name[i], self)
            temp_actn.setStatusTip(action_status_tip[i])
            temp_actn.setShortcut(action_shortcut[i])
            temp_actn.triggered.connect(action_handler_fcn[action_name[i]])
            self.toolbar.addAction(temp_actn)
            self.actions[action_name[i]] = temp_actn
        # options
        self.toolbar.addSeparator()
        self.addToolBarBreak()
        
    def toggleToolbar(self):
        toolbar_state = self.toolbar.isVisible()
        self.toolbar.setVisible(not toolbar_state)
        
    def toggleFormatbar(self):
        formatbar_state = self.formatbar.isVisible()
        self.formatbar.setVisible(not formatbar_state)
        
    def toggleStatusbar(self):
        statusbar_state = self.statusbar.isVisible()
        self.statusbar.setVisible(not statusbar_state)
        
    def new_doc(self):
        new_instance = Editor(self)
        new_instance.show()
        
    def open_doc(self):
        filters = '(*.texteditor *.py *.java *.cpp *.c *.txt *.odt *.html *.php *.css *.js)'
        self.file_name = QFileDialog.getOpenFileName(self, 'Open File', '.', filters)
        if self.file_name:
            with open(self.file_name, 'rt') as file:
                self.main_txt_box.setText(file.read())
                file.close()
                
    def save_doc(self):
        if not self.file_name:
            self.file_name = QFileDialog.getSaveFileName(self, 'Save')
        with open(self.file_name, 'wt') as file:
            file.write(self.main_txt_box.toHtml())
            file.close()
            
    def print_(self):
        print_diag = QPrintDialog()
        if print_diag.exec_() == QDialog.Accepted:
            self.main_txt_box.document().print_(print_diag.printer())
        
    def preview(self):
        print_prev = QPrintPreviewDialog()
        print_prev.paintRequested.connect(lambda p: self.main_txt_box.print_(p))
        print_prev.exec_()
        
    def bulletList(self):
        cursor = self.main_txt_box.textCursor()
        cursor.insertList(QTextListFormat.ListDisc)
        
    def numberedList(self):
        cursor = self.main_txt_box.textCursor()
        cursor.insertList(QTextListFormat.ListDecimal)
        
    def initFormatBar(self):
        font_chooser = QFontComboBox(self)
        font_chooser.currentFontChanged.connect(self.fontFamily)
        
        font_size = QComboBox(self)
        font_size.setEditable(True)
        font_size.setMinimumContentsLength(5)
        font_size.activated.connect(self.fontSize)
        i = 6
        while i != 100:
            font_size.addItem(str(i))
            if i < 16:
                i += 1
            elif i <= 34:
                i += 2
            elif i <= 48:
                i += 4
            else:
                i += 8
        
        self.formatbar = self.addToolBar('Format')
        self.formatbar.addWidget(font_chooser)
        self.formatbar.addWidget(font_size)
        self.formatbar.addSeparator()
        
        format_bar_actions = ['Change font color', 'Change background color', 'Bold', 'Italic', 'Underline', 'Strike-out', 
                              'Superscript', 'Subscript', 'Align left', 
                              'Align right', 'Align center', 'Align justify']
        format_bar_fcn_handler = {'Change font color': self.fontColor, 'Change background color': self.backgroundColor, 
                                  'Bold': self.bold, 'Italic': self.italic, 'Underline': self.underline, 'Strike-out':self.strikeOut, 
                                  'Superscript':self.superscript, 'Subscript':self.subscript, 'Align left': self.alignLeft, 
                                  'Align right': self.alignRight, 'Align center': self.alignCenter, 'Align justify': self.alignJustify}
        self.formatbar_actions = {}
        for i in range(len(format_bar_actions)):
            temp_actn = QAction(format_bar_actions[i], self)
            temp_actn.triggered.connect(format_bar_fcn_handler[format_bar_actions[i]])
            self.formatbar_actions[format_bar_actions[i]] = temp_actn
            self.formatbar.addAction(temp_actn)

        self.formatbar.addSeparator()
        
    def fontFamily(self, font):
        self.main_txt_box.setCurrentFont(font)

    def fontSize(self, sz):
        self.main_txt_box.setFontPointSize(int(sz)+6)
        
    def fontColor(self):
        color = QColorDialog.getColor(initial=Qt.white, parent=None)
        self.main_txt_box.setTextColor(color)
        
    def backgroundColor(self):
        color = QColorDialog.getColor(initial=Qt.white, parent=None)
        self.main_txt_box.setTextBackgroundColor(color)
    
    def bold(self):
        if self.main_txt_box.fontWeight() == QFont.Bold:
            self.main_txt_box.setFontWeight(QFont.Normal)
        else:
            self.main_txt_box.setFontWeight(QFont.Bold)

    def italic(self):
        self.main_txt_box.setFontItalic(not self.main_txt_box.fontItalic())

    def underline(self):
        self.main_txt_box.setFontUnderline(not self.main_txt_box.fontUnderline())

    def strikeOut(self):
        format = self.main_txt_box.currentCharFormat()
        format.setFormatStrikeOut(not format.fontStrikeOut())
        self.main_txt_box.setCurrentCharFormat(format)
        
    def superscript(self):
        format = self.main_txt_box.currentCharFormat()
        alignmnt = format.verticalAlignment()
        if alignmnt == QTextCharFormat.AlignNormal:
            format.setVerticalAlignment(QTextCharFormat.AlignSuperScript)
        else:
            format.setVerticalAlignment(QTextCharFormat.AlignNormal)
        self.main_txt_box.setCurrentCharFormat(format)
        
    def subscript(self):
        format = self.main_txt_box.currentCharFormat()
        alignmnt = format.verticalAlignment()
        if alignmnt == QTextCharFormat.AlignNormal:
            format.setVerticalAlignment(QTextCharFormat.AlignSubScript)
        else:
            format.setVerticalAlignment(QTextCharFormat.AlignNormal)
        self.main_txt_box.setCurrentCharFormat(format)

    def alignLeft(self):
        self.main_txt_box.setAlignment(Qt.AlignLeft)
    
    def alignRight(self):
        self.main_txt_box.setAlignment(Qt.AlignRight)
    
    def alignCenter(self):
        self.main_txt_box.setAlignment(Qt.AlignCenter)
    
    def alignJustify(self):
        self.main_txt_box.setAlignment(Qt.AlignJustify)
    

    def cursorPosition(self):    
        cursor = self.main_txt_box.textCursor()
        line = cursor.blockNumber() + 1
        col = cursor.columnNumber()
        self.statusbar.showMessage('Line: %s \t\t Column: %s' % (str(line), str(col)))
        
def start():
    app = QApplication(sys.argv)
    window = Editor(None,.5)
    window.show()
    sys.exit(app.exec_())
    
if __name__ == '__main__':
    start()

