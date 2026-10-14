from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import StringProperty
import urllib.request
import json

# ضع هنا رابط الويب الخاص بك (Web App URL) الخاص بـ Google Apps Script الذي أخذناه من جوجل
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwHrfKvoDjzMx6qi1E49CaHDlFcJIGDu0qBic14_tsq4Yn3qfbAG4SHHSg87dUbf5NV/exec"

class RowWidget(RecycleDataViewBehavior, Label):
    text = StringProperty('')
    def refresh_view_attrs(self, rv, index, data):
        self.text = data['text']
        return super(RowWidget, self).refresh_view_attrs(rv, index, data)

class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15

        # حقل البحث والاستعلام
        self.search_input = TextInput(hint_text='ابحث عن اسم أو رقم...', size_hint_y=None, height=50)
        self.search_input.bind(text=self.filter_data)
        self.add_widget(self.search_input)

        # زر التحديث لجلب البيانات من Google Sheets
        self.refresh_btn = Button(text='تحديث البيانات من السحابة', size_hint_y=None, height=50, background_color=(0.1, 0.6, 0.3, 1))
        self.refresh_btn.bind(on_press=self.fetch_data_from_cloud)
        self.add_widget(self.refresh_btn)

        # قائمة عرض البيانات (RecycleView)
        self.rv = RecycleView()
        self.rv.size_hint = (1, 1)
        self.rv.viewclass = 'RowWidget'
        self.rv.layout_manager = {'orientation': 'vertical', 'd': {'=': 'dp(40)'}}
        self.data_list = []
        self.add_widget(self.rv)

        # جلب البيانات تلقائياً عند فتح التطبيق
        self.fetch_data_from_cloud(None)

    def fetch_data_from_cloud(self, instance):
        try:
            req = urllib.request.Request(WEB_APP_URL, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                result = json.loads(response.read().decode('utf-8'))
                self.all_records = result
                self.update_list_display(result)
        except Exception as e:
            print("خطأ في جلب البيانات:", e)

    def update_list_display(self, records):
        formatted_data = []
        for item in records:
            text_line = f"الاسم: {item.get('name', '')}  |  الهاتف: {item.get('phone', '')}"
            formatted_data.append({'text': text_line})
        self.data_list = formatted_data
        self.rv.data = self.data_list

    def filter_data(self, instance, value):
        if not hasattr(self, 'all_records'):
            return
        query = value.strip().lower()
        if not query:
            self.update_list_display(self.all_records)
            else:
            filtered = [
                item for item in self.all_records 
                if query in item.get('name', '').lower() or query in str(item.get('phone', ''))
            ]
            self.update_list_display(filtered)

class MyApp(App):
    def build(self):
        self.title = "تطبيق متابعة العملاء"
        return MainScreen()

if __name__ == '__main__':
    MyApp().run()