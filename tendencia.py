import wx
import csv

class MainFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(400, 300))

        self.numbers = []

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
    
        self.input_text = wx.TextCtrl(panel, -1, style=wx.TE_PROCESS_ENTER)
        self.input_text.Bind(wx.EVT_TEXT_ENTER, self.on_enter_press)
        vbox.Add(self.input_text, 0, wx.EXPAND | wx.ALL, 5)

        label = wx.StaticText(panel, -1, "Presione Intro para añadir el número")
        vbox.Add(label, 0, wx.EXPAND | wx.ALL, 5)

        open_csv_button = wx.Button(panel, -1, "Abrir CSV")
        open_csv_button.Bind(wx.EVT_BUTTON, self.on_open_csv)
        vbox.Add(open_csv_button, 0, wx.EXPAND | wx.ALL, 5)

        csv_button = wx.Button(panel, -1, "Guardar resultados en CSV")
        csv_button.Bind(wx.EVT_BUTTON, self.on_csv_button)
        vbox.Add(csv_button, 0, wx.EXPAND | wx.ALL, 5)

        self.results_text = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.results_text, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)
        self.Centre()
        self.Show()

    def on_enter_press(self, event):
        user_input = self.input_text.GetValue().strip()
        if user_input:
            if user_input.isdigit():
                self.numbers.append(int(user_input))
                self.input_text.SetValue("")
                self.update_results()
            else:
                wx.MessageBox("Por favor, introduzca sólo números.", "Error", wx.OK | wx.ICON_ERROR)



    def on_open_csv(self, event):
        open_file_dialog = wx.FileDialog(
            self, "Abrir archivo CSV", "", "", "Archivos CSV (*.csv)|*.csv",
            wx.FD_OPEN | wx.FD_FILE_MUST_EXIST
        )
        if open_file_dialog.ShowModal() == wx.ID_CANCEL:
            return
        
        file_path = open_file_dialog.GetPath()
        self.numbers = []
        
        with open(file_path, "r") as file:
            reader = csv.reader(file)
            header = next(reader)

            for row in reader:
                self.numbers.append(int(row[0]))

        self.on_show_results(event)


    def update_results(self):
        number_counts = {}
        for number in self.numbers:
            number_counts[number] = number_counts.get(number, 0) + 1

        total = len(self.numbers)
        results = ["Número\tVeces\tPorcentaje"]
        sorted_numbers = sorted(
            number_counts.items(), key=lambda x: x[1] / total * 100, reverse=True
        )
        for number, count in sorted_numbers:
            results.append("{}\t{}\t{:.2f}%".format(number, count, count / total * 100))

        self.results_text.SetValue("\n".join(results))



    def on_show_results(self, event):
        numbers = self.numbers
        counts = {number: numbers.count(number) for number in set(numbers)}

        total = len(numbers)
        results = "Número\tVeces\tPorcentaje\n"
        for number, count in counts.items():
            results += f"{number}\t{count}\t{count / total * 100:.2f}%\n"

        self.results_text.SetValue(results)

    def on_csv_button(self, event):
        numbers = self.numbers
        counts = {number: numbers.count(number) for number in set(numbers)}

        total = len(numbers)
        rows = [["Número", "Veces", "Porcentaje"]]
        for number, count in counts.items():
            rows.append([number, count, count / total * 100])

        rows.append(numbers)

        with open("resultados.csv", "a", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(rows)


app = wx.App()
frame = MainFrame(None, "Tendencia numérica")
app.MainLoop()


