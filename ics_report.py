import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import datetime
from ics import ICS_insert, ICS_edit
from templates.database import Database
from templates.utility import Utility


class ICS_report():
    tree_heading = ["ID","ICS No.","IAR No.", "Office", "Date", "Article", "Qty","Unit","Amount","Date Acquired","Est. Useful life"]
    dict_category = {
        "ICS Number": 0,
        "IAR Number": 1,
        "Office": 2,
        "ICS Date": 3,
        "Article": 4,
        "Quantity": 5,
        "Unit": 6,
        "Amount": 7,
        "Date Acquired": 8
    }
    def __init__(self,parent):
        self.parent = parent
        self.db_obj = Database()
        self.style = ttk.Style()
        self.initUI()
        self.tree_populate()
        self.parent.grid_columnconfigure(0,weight=1)



    def initUI(self):
        ''' ============================ Frame 1 ============================='''
        frame1 = ttk.Frame(self.parent)

        ttk.Label(frame1, text="Search By: ").grid(row=0,column=0)
        self.cmb_search_category_var = tk.StringVar()
        self.cmb_search_category = ttk.Combobox(frame1, state="readonly",values=[x for x in self.dict_category.keys()],textvariable=self.cmb_search_category_var)
        self.cmb_search_category.bind("<<ComboboxSelected>>",lambda event, x=frame1:self.seach_ui_controller(x))

        self.cmb_search_category.grid(row=0,column=1)
        frame1.grid(row=0,column=0,sticky="nsew")
        frame1.grid_columnconfigure(2,weight=1)

        ''' ============================ Frame 2 ============================='''
        frame2 = ttk.Frame(self.parent)

        self.tree_ics_report = ttk.Treeview(frame2, height=20, column=self.tree_heading)
        self.tree_ics_report['show'] = "headings"

        i = 1
        for col in self.tree_heading:
            num = f"#{i}"
            self.tree_ics_report.heading(num, text=col)
            if i == 1:
                self.tree_ics_report.column(num, width=30, anchor=tk.CENTER)
            else:
                self.tree_ics_report.column(num, width=115, anchor=tk.CENTER)
            i += 1

        self.scroll_y_tree = ttk.Scrollbar(frame2, orient="vertical", command=self.tree_ics_report.yview)
        self.scroll_x_tree = ttk.Scrollbar(frame2, orient="horizontal", command=self.tree_ics_report.xview)
        self.tree_ics_report.configure(yscrollcommand=self.scroll_y_tree.set)
        self.tree_ics_report.configure(xscrollcommand=self.scroll_x_tree.set)

        self.tree_ics_report.bind("<Double-Button-1>", self.event_tree_item)

        self.tree_ics_report.grid(row=0, column=0, sticky="nsew")
        self.scroll_y_tree.grid(row=0, column=1, sticky="ns")
        self.scroll_x_tree.grid(row=1, column=0, sticky="ew")

        frame2.grid(row=1, column=0, sticky="nsew")
        frame2.grid_columnconfigure(0, weight=1)


        ''' ============================ Frame 3 ============================='''
        frame3 = ttk.Frame(self.parent)

        self.btn_add = ttk.Button(frame3,text="+",command=self.callback_btn_add)
        self.btn_generate_report = ttk.Button(frame3, text="Generate Report", command=self.callback_btn_generate_report)
        self.btn_filter = ttk.Button(frame3, text="Filter", command=self.callback_btn_filter)
        self.btn_refresh = ttk.Button(frame3,text="Refresh",command=self.callback_btn_refresh)

        self.btn_add.grid(row=0,column=0,sticky="nsw")
        self.btn_generate_report.grid(row=0,column=1,sticky="nsw")
        self.btn_filter.grid(row=0,column=2,sticky="nsw")
        self.btn_refresh.grid(row=0,column=4,sticky="nse")

        frame3.grid(row=2,column=0,sticky="nsew")
        frame3.grid_columnconfigure(2,weight=1)

    ''' ***************************** Regular Methods ********************************'''
    def search_events(self,controller):
        items=[]
        if controller == 0:
            ics_no = self.ent_search_ics_no_var.get()
            items = self.db_obj.search_items(0,ics_no)
        elif controller == 1:
            iar_no = self.ent_search_iar_no_var.get()
            items = self.db_obj.search_items(1,iar_no)
        elif controller == 2:
            office_desc = self.cmb_search_office.get()
            items = self.db_obj.search_items(2,office_desc)
        elif controller == 3:
            date_month = self.cmb_search_date_month.get()
            date_day = self.cmb_search_date_day.get()
            date_year = self.cmb_search_date_year.get()
            if date_month != "" and date_day != "" and date_year != "":
                dict_month = Utility.month_dictionary(0)
                date = datetime.datetime(int(date_year),dict_month[date_month],int(date_day))
                formatted_date = Utility.date_formatter(date,1)
                items = self.db_obj.search_items(3,formatted_date)
        elif controller == 4:
            item_article = self.ent_search_article_var.get()
            items = self.db_obj.search_items(4,item_article)
        elif controller == 5:
            item_quantity = self.spn_search_quantity_var.get()
            items = self.db_obj.search_items(5, item_quantity)
        elif controller == 6:
            item_unit = self.ent_search_unit_var.get()
            items = self.db_obj.search_items(6, item_unit)
        elif controller == 7:
            item_unit = self.spn_search_amount_var.get()
            items = self.db_obj.search_items(7, item_unit)
        elif controller == 8:
            date_month = self.cmb_search_date_acquired_month.get()
            date_day = self.cmb_search_date_acquired_day.get()
            date_year = self.cmb_search_date_acquired_year.get()
            if date_month != "" and date_day != "" and date_year != "":
                dict_month = Utility.month_dictionary(0)
                date = datetime.datetime(int(date_year), dict_month[date_month], int(date_day))
                formatted_date = Utility.date_formatter(date, 1)
                items = self.db_obj.search_items(8, formatted_date)

        self.tree_populate_search(items)

    def seach_ui_controller(self,frame):
        inner_frame = ttk.Frame(frame)
        controller = self.dict_category[self.cmb_search_category_var.get()]
        if controller == 0:
            self.ent_search_ics_no_var = tk.StringVar()
            self.ent_search_ics_no = ttk.Entry(inner_frame,textvariable=self.ent_search_ics_no_var)
            self.ent_search_ics_no.bind('<KeyRelease>',lambda event:self.search_events(0))
            self.ent_search_ics_no.grid(row=0,column=2,sticky="nsew")
        elif controller == 1:
            self.ent_search_iar_no_var = tk.StringVar()
            self.ent_search_iar_no = ttk.Entry(inner_frame, textvariable=self.ent_search_iar_no_var)
            self.ent_search_iar_no.bind('<KeyRelease>', lambda event: self.search_events(1))
            self.ent_search_iar_no.grid(row=0,column=2)
        elif controller == 2:
            self.cmb_search_office = ttk.Combobox(inner_frame,state="readonly",values=self.db_obj.get_offices())
            self.cmb_search_office.bind('<<ComboboxSelected>>', lambda event: self.search_events(2))
            self.cmb_search_office.grid(row=0,column=2)
        elif controller == 3:
            self.cmb_search_date_month = ttk.Combobox(inner_frame, state="readonly",values=[x for x in Utility.month_dictionary(0).keys()])
            self.cmb_search_date_day = ttk.Combobox(inner_frame, state="readonly", values=[x for x in range(1,32)])
            self.cmb_search_date_year = ttk.Combobox(inner_frame, state="readonly", values=[x for x in range(2020,2050)])

            self.cmb_search_date_month.bind('<<ComboboxSelected>>', lambda event: self.search_events(3))
            self.cmb_search_date_day.bind('<<ComboboxSelected>>',lambda event: self.search_events(3))
            self.cmb_search_date_year.bind('<<ComboboxSelected>>',lambda event: self.search_events(3))

            self.cmb_search_date_month.grid(row=0,column=2)
            self.cmb_search_date_day.grid(row=0,column=3)
            self.cmb_search_date_year.grid(row=0,column=4)
        elif controller == 4:
            self.ent_search_article_var = tk.StringVar()
            self.ent_search_article = tk.Entry(inner_frame,textvariable=self.ent_search_article_var)
            self.ent_search_article.bind('<KeyRelease>', lambda event: self.search_events(4))
            self.ent_search_article.grid(row=0,column=2)
        elif controller == 5:
            self.spn_search_quantity_var = tk.StringVar()
            self.spn_search_quantity = ttk.Spinbox(inner_frame, from_=1, to=9999999, textvariable=self.spn_search_quantity_var)
            self.spn_search_quantity.bind('<KeyRelease>', lambda event: self.search_events(5))
            self.spn_search_quantity.bind('<ButtonRelease-1>',lambda event: self.search_events(5))
            self.spn_search_quantity.grid(row=0,column=2)
        elif controller == 6:
            self.ent_search_unit_var = tk.StringVar()
            self.ent_search_unit = ttk.Entry(inner_frame, textvariable=self.ent_search_unit_var)
            self.ent_search_unit.bind('<KeyRelease>', lambda event: self.search_events(6))
            self.ent_search_unit.grid(row=0,column=2)
        elif controller == 7:
            self.spn_search_amount_var = tk.StringVar()
            self.spn_search_amount = ttk.Spinbox(inner_frame, from_=1, to=9999999, textvariable=self.spn_search_amount_var)
            self.spn_search_amount.bind('<KeyRelease>',lambda event: self.search_events(7))
            self.spn_search_amount.bind('<ButtonRelease-1>', lambda event: self.search_events(7))
            self.spn_search_amount.grid(row=0, column=2)
        elif controller == 8:
            self.cmb_search_date_acquired_month = ttk.Combobox(inner_frame, state="readonly", values=[x for x in Utility.month_dictionary(0).keys()])
            self.cmb_search_date_acquired_day = ttk.Combobox(inner_frame, state="readonly", values=[x for x in range(1,32)])
            self.cmb_search_date_acquired_year = ttk.Combobox(inner_frame, state="readonly", values=[x for x in range(2020,2050)])

            self.cmb_search_date_acquired_month.bind('<<ComboboxSelected>>', lambda event: self.search_events(8))
            self.cmb_search_date_acquired_day.bind('<<ComboboxSelected>>', lambda event: self.search_events(8))
            self.cmb_search_date_acquired_year.bind('<<ComboboxSelected>>', lambda event: self.search_events(8))

            self.cmb_search_date_acquired_month.grid(row=0,column=2)
            self.cmb_search_date_acquired_day.grid(row=0, column=3)
            self.cmb_search_date_acquired_year.grid(row=0, column=4)

        inner_frame.grid(row=0,column=2,sticky="nsew")

    def tree_populate_search(self,items):
        self.tree_ics_report.delete(*self.tree_ics_report.get_children())
        items = [list(x) for x in items]
        for item in items:
            item[4] = Utility.date_formatter(item[4],2)
            item[9] = Utility.date_formatter(item[9],2)
            self.tree_ics_report.insert("", tk.END, values=item)

    def tree_populate(self):
        self.tree_ics_report.delete(*self.tree_ics_report.get_children())
        tree_items = [list(x) for x in self.db_obj.get_ics_items()]
        print(tree_items)
        for item in tree_items:
            item[4] = Utility.date_formatter(item[4],2)
            item[9] =  Utility.date_formatter(item[9],2)
            self.tree_ics_report.insert("",tk.END,values=item)

    ''' ***************************** Callback Methods ********************************'''

    def callback_btn_add(self):
        top = tk.Toplevel()
        top.attributes('-topmost',1)
        edit_window = ICS_insert(top)
        top.attributes('-topmost',0)
        self.parent.wait_window(top)
        self.tree_populate()
        top.mainloop()

    def callback_btn_filter(self):
        top = tk.Toplevel()
        top.attributes('-topmost',1)
        sort_window = Filter_Items(top)
        top.attributes('-topmost',0)
        self.parent.wait_window(top)
        top.mainloop()

    def callback_btn_generate_report(self):
        all_ics_items = self.db_obj.get_ics_report()
        Utility.generate_printable_report(all_ics_items)

    def callback_btn_refresh(self):
        self.tree_populate()

    ''' ***************************** Event Methods ********************************'''

    def event_tree_item(self,event):
        selected_item_obj = self.tree_ics_report.focus()
        selected_item_val = self.tree_ics_report.item(selected_item_obj)['values']

        top = tk.Toplevel()
        top.attributes('-topmost',1)
        add_window = ICS_edit(top,selected_item_val[0])
        top.attributes('-topmost',0)
        self.parent.wait_window(top)
        self.tree_populate()
        top.mainloop()

class Filter_Items():
    def __init__(self,parent):
        self.parent = parent
        self.parent.grab_set()
        self.db_obj = Database()
        self.initUI()

    def initUI(self):
        frame1 = ttk.Frame(self.parent)

        # Title
        tk.Label(frame1, text="FILTER").grid(row=0,column=0,columnspan=3,sticky="nsew")
        # Office
        ttk.Label(frame1,text="Office").grid(row=1,column=0,sticky="nsew")
        self.cmb_office = ttk.Combobox(frame1, state="readonly", values=self.db_obj.get_offices())
        self.cmb_office.grid(row=1, column=1,columnspan=2,sticky="ew")

        # ICS Date
        inner_frame1 = ttk.Frame(frame1)
        ttk.Label(inner_frame1,text="ICS Date").grid(row=0,column=0)
        ttk.Label(inner_frame1,text="From").grid(row=1,column=0)
        ttk.Label(inner_frame1,text="To").grid(row=2,column=0)

        self.cmb_ics_date_from_month = ttk.Combobox(inner_frame1, state="readonly", values=[x for x in Utility.month_dictionary(0)])
        self.cmb_ics_date_from_day = ttk.Combobox(inner_frame1, state="readonly", values=Utility.days_generator())
        self.cmb_ics_date_from_year = ttk.Combobox(inner_frame1,state="readonly",values=Utility.years_generator())


        self.cmb_ics_date_to_month = ttk.Combobox(inner_frame1, state="readonly", values=[x for x in Utility.month_dictionary(0)])
        self.cmb_ics_date_to_day = ttk.Combobox(inner_frame1, state="readonly", values=Utility.days_generator())
        self.cmb_ics_date_to_year = ttk.Combobox(inner_frame1,state="readonly",values=Utility.years_generator())

        self.cmb_ics_date_from_month.grid(row=1,column=1,sticky="ew")
        self.cmb_ics_date_from_day.grid(row=1,column=2,sticky="ew")
        self.cmb_ics_date_from_year.grid(row=1,column=3,sticky="ew")

        self.cmb_ics_date_to_month.grid(row=2, column=1,sticky="ew")
        self.cmb_ics_date_to_day.grid(row=2, column=2, sticky="ew")
        self.cmb_ics_date_to_year.grid(row=2, column=3, sticky="ew")

        inner_frame1.grid(row=2,column=0,columnspan=3,sticky="ew")
        inner_frame1.grid_columnconfigure(1,weight=1)

        # Article
        ttk.Label(frame1, text="Article").grid(row=3,column=0,sticky="nsew")
        self.ent_article_var = tk.StringVar()
        self.ent_article = ttk.Entry(frame1,textvariable=self.ent_article_var)
        self.ent_article.grid(row=3,column=1,columnspan=2,sticky="ew")

        # Quantity
        ttk.Label(frame1,text="Qty.").grid(row=4,column=0,sticky="nsew")
        self.spn_qty = ttk.Spinbox(frame1,from_=1,to=9999999)
        self.spn_qty.grid(row=4,column=1,columnspan=2,sticky="ew")

        # Unit
        ttk.Label(frame1, text="Unit").grid(row=5,column=0,sticky="nsew")
        self.ent_unit_var = tk.StringVar()
        self.ent_unit = ttk.Entry(frame1,textvariable=self.ent_unit_var)
        self.ent_unit.grid(row=5,column=1,columnspan=2,sticky="ew")

        # Amount
        ttk.Label(frame1,text="Amount").grid(row=6,column=0,sticky="nsew")
        self.spn_amount = ttk.Spinbox(frame1,from_=1,to=9999999999)
        self.spn_amount.grid(row=6,column=1,columnspan=2,sticky="ew")

        # Date Acquired
        inner_frame2 = ttk.Frame(frame1)

        ttk.Label(inner_frame2, text="Date Acqd.").grid(row=0, column=0)
        ttk.Label(inner_frame2, text="From").grid(row=1, column=0)
        ttk.Label(inner_frame2, text="To").grid(row=2, column=0)

        self.cmb_date_acquired_from_month = ttk.Combobox(inner_frame2, state="readonly", values=[x for x in Utility.month_dictionary(0)])
        self.cmb_date_acquired_from_day = ttk.Combobox(inner_frame2, state="readonly", values=Utility.days_generator())
        self.cmb_date_acquired_from_year = ttk.Combobox(inner_frame2, state="readonly", values=Utility.years_generator())

        self.cmb_date_acquired_to_month = ttk.Combobox(inner_frame2, state="readonly", values=[x for x in Utility.month_dictionary(0)])
        self.cmb_date_acquired_to_day = ttk.Combobox(inner_frame2, state="readonly", values=Utility.days_generator())
        self.cmb_date_acquired_to_year = ttk.Combobox(inner_frame2, state="readonly", values=Utility.years_generator())


        self.cmb_date_acquired_from_month.grid(row=1,column=1,sticky="ew")
        self.cmb_date_acquired_from_day.grid(row=1,column=2,sticky="ew")
        self.cmb_date_acquired_from_year.grid(row=1, column=3, sticky="ew")

        self.cmb_date_acquired_to_month.grid(row=2,column=1,sticky="ew")
        self.cmb_date_acquired_to_day.grid(row=2,column=2,sticky="ew")
        self.cmb_date_acquired_to_year.grid(row=2, column=3,sticky="ew")

        inner_frame2.grid(row=7,column=0,columnspan=3,sticky="ew")
        inner_frame2.grid_columnconfigure(1,weight=1)

        # Est. Durability
        ttk.Label(frame1,text="Est. Useful Life").grid(row=8,column=0,sticky="nsew")
        self.ent_durability_var = tk.StringVar()
        self.ent_durability = ttk.Entry(frame1,textvariable=self.ent_durability_var)
        self.ent_durability.grid(row=8,column=1,columnspan=2,sticky="ew")

        # Buttons
        self.btn_filter = ttk.Button(frame1,text="Filter",command=self.callback_btn_filter)
        self.btn_clear = ttk.Button(frame1,text="clear",command=self.callback_btn_clear)
        self.btn_cancel = ttk.Button(frame1,text="Cancel",command=self.callback_btn_cancel)

        self.btn_filter.grid(row=9,column=0,sticky="nsw")
        self.btn_clear.grid(row=9,column=1,sticky="nsw")
        self.btn_cancel.grid(row=9,column=2,sticky="nse")


        frame1.grid(row=0,column=0,sticky="nsew")
        frame1.grid_columnconfigure(1,weight=1)
        for i in frame1.winfo_children():
            i.grid_configure(padx=10,pady=10)
        self.parent.grid_columnconfigure(0,weight=1)


    '''********************************************************************************
     ******************************** CALLBACK METHODS ******************************** 
     ********************************************************************************'''
    def callback_btn_filter(self):
        

        # Get the ICS Date [From]
        ics_date_from_month = self.cmb_ics_date_from_month.get()
        ics_date_from_day = self.cmb_ics_date_from_day.get()
        ics_date_from_year = self.cmb_ics_date_from_year.get()

        # If ics_date_from combobox is empty
        if ics_date_from_month == "" or ics_date_from_day == "" or ics_date_from_year == "":
            # set the ics_date_from to 2010 (The very beginning)
            ics_date_from = "2010-01-01"

        # If the ics_date_From combobox is not empty
        else:
            # Convert the ics_date_from combobox from STRING to INTEGER
            ics_date_from = Utility.date_formatter(datetime.datetime(int(ics_date_from_year),
                                              Utility.month_dictionary(1,ics_date_from_month),
                                              int(ics_date_from_day)),1)


        # Get the ICS Date [To]
        ics_date_to_month = self.cmb_ics_date_to_month.get()
        ics_date_to_day = self.cmb_ics_date_to_day.get()
        ics_date_to_year = self.cmb_ics_date_to_year.get()


        if ics_date_to_month == "" or ics_date_to_day == "" or ics_date_to_year == "":
            ics_date_to_month = datetime.date.today().month
            ics_date_to_day = datetime.date.today().day
            ics_date_to_year = datetime.date.today().year

            ics_date_to = f"{ics_date_to_year}-{ics_date_to_month}-{ics_date_to_day}"
            print(ics_date_to)

        else:
            ics_date_to = Utility.date_formatter(datetime.datetime(int(ics_date_to_year),
                                            Utility.month_dictionary(1,ics_date_to_month),
                                            int(ics_date_to_day)),1)


        
        article = self.ent_article_var.get()

        quantity = self.spn_qty.get()

        unit = self.ent_unit_var.get()

        amount = self.spn_amount.get()


        date_acquired_from_month = self.cmb_date_acquired_from_month.get()
        date_acquired_from_day = self.cmb_date_acquired_from_day.get()
        date_acquired_from_year = self.cmb_date_acquired_from_year.get()

        if date_acquired_from_month == "" or date_acquired_from_day == "" or date_acquired_from_year == "":
            date_acquired_from = "2010-01-01"
        else:
            date_acquired_from = Utility.date_formatter(datetime.datetime(int(date_acquired_from_year),
                                                                     Utility.month_dictionary(1, date_acquired_from_month),
                                                                     int(date_acquired_from_day)), 1)

        date_acquired_to_month = self.cmb_date_acquired_to_month.get()
        date_acquired_to_day = self.cmb_date_acquired_to_day.get()
        date_acquired_to_year = self.cmb_date_acquired_to_year.get()

        if date_acquired_to_month == "" or date_acquired_to_day == "" or date_acquired_to_year == "":
            date_acquired_to_month = datetime.date.today().month
            date_acquired_to_day = datetime.date.today().day
            date_acquired_to_year = datetime.date.today().year

            date_acquired_to = f"{date_acquired_to_year}-{date_acquired_to_month}-{date_acquired_to_day}"
        else:
            date_acquired_to = Utility.date_formatter(datetime.datetime(int(date_acquired_to_year),
                                            Utility.month_dictionary(1,date_acquired_to_month),
                                            int(date_acquired_to_day)),1)


        durability = self.ent_durability_var.get()

        dict_information = {
            # Get the office
            "office": self.cmb_office.get(),
            "ics_date_from": ics_date_from,
            "ics_date_to": ics_date_to,
            "article": article,
            "quantity": quantity,
            "unit": unit,
            "amount": amount,
            "date_acquired_from": date_acquired_from,
            "date_acquired_to": date_acquired_to,
            "durability": durability
        }

        for item in dict_information:
            print(item, "     ", dict_information[item])



    def callback_btn_clear(self):
        self.cmb_office.set("")
        self.cmb_ics_date_from_year.set("")
        self.cmb_ics_date_to_year.set("")
        self.ent_article_var.set("")
        self.spn_qty.set("")
        self.ent_unit_var.set("")
        self.spn_amount.set("")
        self.cmb_date_acquired_from_year.set("")
        self.cmb_date_acquired_to_year.set("")
        self.ent_durability_var.set("")

    def callback_btn_cancel(self):
        cancel_confirmation = messagebox.askyesno("Cancel Confirmation","Are you sure you want to cancel filtering?")
        if cancel_confirmation is True:
            self.parent.destroy()





































if __name__ == "__main__":
    app = tk.Tk()
    window = ICS_report(app)
    app.mainloop()
