import os
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import ttk

from templates.utility import Utility
from templates.database import Database
from templates.tabFrameTemplate import TabFrameTemplate


class ICS:
    dict_month = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    list_day = list(range(1,32))
    list_year = list(range(2010,2040))
    header = ['Quantity', 'Unit','Article', 'Description', 'Amount', 'Date Acquired', 'Est. Useful Life']
    def __init__(self,parent):
        self.parent = parent
        self.db_obj = Database()
        self.main_frame = TabFrameTemplate(self.parent)
        self.main_frame.grid(row=0,column=0)

        self.style=ttk.Style()
        self.style.configure("ICS.TFrame",
                             background="#FE7B79",
                             )
        self.style.configure("Item.TFrame",
                             relief="sunken",
                             background="#FFCFCF",
                             font=('Sans','15','bold')
                             )
        self.style.configure("Inner.TFrame",
                             background="#FFCFCF",
                             )
        self.style.configure("ICS.TLabel",
                             background="#FE7B79",
                             font = ('Sans','15','bold')
                             )
        self.style.configure("Item.TLabel",
                             background="#FFCFCF",
                             font=('Sans', '15', 'bold')
                             )

        self.initUI()


    def initUI(self):
        ''' ============================ Frame 1 ============================='''
        frame1 = ttk.Frame(self.main_frame.view_port,style="ICS.TFrame")

        # ========== START: Row 0 ========== #

        # --- ICS No. --- #
        ttk.Label(frame1, text="ICS No.",style="ICS.TLabel").grid(row=0, column=0,sticky="nsew")
        self.ent_ics_no_var = tk.StringVar()
        self.ent_ics_no = ttk.Entry(frame1, textvariable=self.ent_ics_no_var)

        # --- ICS Image Button --- #
        self.btn_scan_ics = ttk.Button(frame1, text="ICS", style="ICS.TButton")

        self.ent_ics_no.grid(row=0, column=1, sticky="nsew")
        self.btn_scan_ics.grid(row=0, column=2, padx=4, sticky="nsew")

        # ========== END: Row 0 ========== #

        # ========== START: Row 1 ========== #

        # --- IAR No. --- #
        ttk.Label(frame1, text="IAR No.",style="ICS.TLabel").grid(row=1,column=0,sticky="nsew")
        self.ent_iar_no_var = tk.StringVar()
        self.ent_iar_no = ttk.Entry(frame1, textvariable=self.ent_iar_no_var)

        # --- IAR Image Button --- #
        self.btn_scan_iar = ttk.Button(frame1, text="IAR")

        self.ent_iar_no.grid(row=1, column=1, sticky="nsew")
        self.btn_scan_iar.grid(row=1,column=2,sticky="nsew")

        # ========== END: Row 1 ========== #

        # ========== START: Row 2 ========== #

        ttk.Label(frame1, text="Office",style="ICS.TLabel").grid(row=2, column=0,sticky="nsew")
        self.cmb_ics_office = ttk.Combobox(frame1,state="normal", values=self.db_obj.get_offices())
        self.cmb_ics_office.grid(row=2, column=1,columnspan=2,sticky="nsew")

        # ========== END: Row 2 ========== #

        # ========== START: Row 3 ========== #

        ttk.Label(frame1,text="Date",style="ICS.TLabel").grid(row=3,column=0,sticky="nsew")
        date_frame = ttk.Frame(frame1,style="ICS.TFrame")

        self.cmb_ics_month = ttk.Combobox(date_frame,state="readonly", values=[x for x in self.dict_month.keys()])
        self.cmb_ics_day = ttk.Combobox(date_frame,state="readonly", values=self.list_day)
        self.cmb_ics_year = ttk.Combobox(date_frame,state="readonly", values=self.list_year)

        self.cmb_ics_month.grid(row=0, column=0,sticky="nsew")
        self.cmb_ics_day.grid(row=0, column=1,sticky="nsew")
        self.cmb_ics_year.grid(row=0, column=2,sticky="nsew")

        date_frame.grid(row=3,column=1,sticky="nsew")
        for widget in date_frame.winfo_children():
            widget.grid_configure(padx=10,pady=10)

        # ========== END: Row 3 ========== #


        frame1.grid(row=0,column=0,sticky="nsew")
        for widget in frame1.winfo_children():
            widget.grid_configure(padx=10,pady=6)
        frame1.grid_columnconfigure(1,weight=1)

        ''' ============================ Frame 2 ============================='''

        frame2 = ttk.LabelFrame(self.main_frame.view_port, text="Items", style="Item.TFrame")

        # ========== START: Row 0 ========== #

        ttk.Label(frame2,text="Article",style="Item.TLabel").grid(row=0,column=0,sticky="nsew")
        self.ent_article_var = tk.StringVar()
        self.ent_article = ttk.Entry(frame2,textvariable=self.ent_article_var)
        self.ent_article.grid(row=0,column=1,sticky="nsew")

        ttk.Label(frame2, text="Quantity",style="Item.TLabel").grid(row=1,column=0,sticky="nsew")
        self.spn_quantity_var = tk.IntVar()
        self.spn_quantity = tk.Spinbox(frame2,from_=1,to=9999999,textvariable=self.spn_quantity_var)
        self.spn_quantity.grid(row=1,column=1,sticky="nsew")

        ttk.Label(frame2, text="Unit",style="Item.TLabel").grid(row=1, column=2,sticky="nsew")
        self.ent_unit_var = tk.StringVar()
        self.ent_unit = ttk.Entry(frame2,textvariable=self.ent_unit_var)
        self.ent_unit.grid(row=1, column=3,sticky="nsew")

        ttk.Label(frame2, text="Description",style="Item.TLabel").grid(row=2, column=0,sticky="nsew")
        self.txt_description = tk.scrolledtext.ScrolledText(frame2,height=5,width=80)
        self.txt_description.grid(row=3, column=0,columnspan=4,sticky="nsew")

        ttk.Label(frame2, text="Amount",style="Item.TLabel").grid(row=4, column=0,sticky="nsew")
        self.ent_amount_var = tk.DoubleVar()
        self.ent_amount = ttk.Entry(frame2,textvariable=self.ent_amount_var)
        self.ent_amount.grid(row=4, column=1,columnspan=2,sticky="nsew")

        ttk.Label(frame2, text="Date Acquired",style="Item.TLabel").grid(row=5,column=0,sticky="nsew")
        items_date_frame = ttk.Frame(frame2,style="Inner.TFrame")
        self.cmb_acquired_month = ttk.Combobox(items_date_frame, state="readonly", values=[x for x in self.dict_month.keys()])
        self.cmb_acquired_day = ttk.Combobox(items_date_frame, state="readonly", values=self.list_day)
        self.cmb_acquired_year = ttk.Combobox(items_date_frame, state="readonly", values=self.list_year)
        self.cmb_acquired_month.grid(row=0, column=0,sticky="nsew")
        self.cmb_acquired_day.grid(row=0, column=1,sticky="nsew")
        self.cmb_acquired_year.grid(row=0, column=2,sticky="nsew")
        items_date_frame.grid(row=5,column=1,columnspan=3,sticky="nsew")
        for widget in items_date_frame.winfo_children():
            widget.grid_configure(padx=10,pady=6)

        ttk.Label(frame2, text="Est.Useful life",style="Item.TLabel").grid(row=6, column=0,sticky="nsew")
        self.ent_useful_life_var = tk.StringVar()
        self.ent_useful_life = ttk.Entry(frame2, textvariable=self.ent_useful_life_var)
        self.ent_useful_life.grid(row=6, column=1, columnspan=2, sticky="nsew")

        inner_buttons_frame = ttk.Frame(frame2,style="Inner.TFrame")
        self.btn_add_item = ttk.Button(inner_buttons_frame, text="Add",command=self.callback_add_item)
        self.btn_delete_item = ttk.Button(inner_buttons_frame, text="Delete",command=self.callback_delete_item)
        self.btn_clear_item = ttk.Button(inner_buttons_frame, text="Clear",command=self.callback_clear_item)
        self.btn_add_item.grid(row=0, column=0,sticky="nsew")
        self.btn_delete_item.grid(row=0, column=1,sticky="nsew")
        self.btn_clear_item.grid(row=0, column=2,columnspan=2,sticky="nsew")
        inner_buttons_frame.grid(row=7,column=0,columnspan=3,sticky="nsew")
        for widget in inner_buttons_frame.winfo_children():
            widget.grid_configure(padx=10,pady=6)


        self.tree_ics_item = ttk.Treeview(frame2, column=self.header)
        self.tree_ics_item['show'] = 'headings'
        i = 1
        for col in self.header:
            num = f'#{i}'
            self.tree_ics_item.heading(num, text=col)
            self.tree_ics_item.column(num, width=115)
            i += 1
        self.tree_ics_item.grid(row=8, column=0, columnspan=4,sticky="nsew")

        frame2.grid(row=1,column=0,sticky="nsew")
        for widget in frame2.winfo_children():
            widget.grid_configure(padx=10,pady=6)
        frame2.grid_columnconfigure(1,weight=1)
        ''' ============================ Frame 3 ============================='''

        self.frame3 = ttk.Frame(self.main_frame.view_port,style="ICS.TFrame")
        self.btn_save_ics = ttk.Button(self.frame3, text="Save")
        self.btn_save_ics.grid(row=0, column=0,sticky="nsew")
        self.frame3.grid(row=2,column=0,sticky="nsew")
        self.frame3.grid_columnconfigure(0,weight=1)

    ''' ************************************************ Callback ************************************************ '''

    def callback_clear_item(self):
        self.ent_article_var.set("")
        self.spn_quantity_var.set(1)
        self.ent_unit_var.set("")
        self.txt_description.delete("1.0","end-1c")
        self.ent_amount_var.set(0.0)
        self.cmb_acquired_month.set("")
        self.cmb_acquired_day.set("")
        self.cmb_acquired_year.set("")
        self.ent_useful_life_var.set("")

    def callback_add_item(self):
        self.items = {
            'quantity': self.spn_quantity.get(),
            'unit': self.ent_unit.get(),
            'article': self.ent_article.get(),
            'description': self.txt_description.get("1.0","end-1c"),
            'amount': self.ent_amount.get(),
            'acquisition': datetime.datetime(int(self.cmb_acquired_year.get()),int(self.dict_month[self.cmb_acquired_month.get()]),int(self.cmb_acquired_day.get())),
            'durability': self.ent_useful_life.get()
        }
        self.items['acquisition'] = self.items['acquisition'].strftime("%Y-%m-%d")
        x = [x for x in self.items.values()]
        self.tree_ics_item.insert('', tk.END, values=x)

    def callback_delete_item(self):
        try:
            selected_item = self.tree_ics_item.focus()
            self.tree_ics_item.delete(selected_item)
        except:
            messagebox.showerror("Selection Error","Please select an item to be deleted")


class ICS_edit:
    dict_month = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 5,
        'June': 6,
        'July': 7,
        'August': 8,
        'September': 9,
        'October': 10,
        'November': 11,
        'December': 12
    }
    def __init__(self, parent, item_id):
        self.parent=parent
        self.parent.grab_set()
        self.item_id = item_id
        self.db_obj = Database()
        self.ics_obj = ICS(self.parent)

        self.initUI()
        self.load_information()
        self.stateUI(0)

    def initUI(self):
        self.ics_obj.tree_ics_item.destroy()
        self.ics_obj.btn_add_item.destroy()
        self.ics_obj.btn_delete_item.destroy()
        self.ics_obj.btn_clear_item.destroy()

        self.btn_delete = ttk.Button(self.ics_obj.frame3,text="Delete Item",command=self.callback_delete)
        self.btn_delete.grid(row=0,column=1,sticky="nsew")

    def load_information(self):
        # self.ics_obj.btn_scan_ics.configure(lambda : os.startfile(os.getcwd() + f"\\scans\\scan_ics\\{self.ics_obj.ent_ics_no_var.get()}"))
        '''
            [0] = ics_no
            [1] = iar_no
            [2] = ics_scan
            [3] = iar_scan
            [4] = office_description
            [5] = ics_date
            [6] = article
            [7] = description
            [8] = quantity
            [9] = unit
            [10] = amount
            [11] = date acquired
            [12] = Est Durability

        :return:
        '''

        ics_info = self.db_obj.get_ics(self.item_id)
        self.ics_obj.ent_ics_no_var.set(ics_info[0])
        self.ics_obj.ent_iar_no_var.set(ics_info[1])

        # --- Scan Button Configuration --- #
        self.old_ics_directory = ics_info[2]
        self.old_iar_directory = ics_info[3]
        self.ics_obj.btn_scan_ics.configure(command=lambda: os.startfile(ics_info[2]))
        self.ics_obj.btn_scan_iar.configure(command=lambda: os.startfile(ics_info[3]))

        self.ics_obj.cmb_ics_office.set(ics_info[4])

        # --- Date Configuration --- #
        new_date = Utility.date_formatter(ics_info[5],0)
        self.ics_obj.cmb_ics_month.set(new_date[0])
        self.ics_obj.cmb_ics_day.set(new_date[1])
        self.ics_obj.cmb_ics_year.set(new_date[2])

        self.ics_obj.ent_article_var.set(ics_info[6])
        self.ics_obj.spn_quantity_var.set(ics_info[8])
        self.ics_obj.ent_unit_var.set(ics_info[9])
        self.ics_obj.txt_description.insert(tk.END,ics_info[7])
        self.ics_obj.ent_amount_var.set(ics_info[10])

        # --- Date Acquired Configuration --- #
        new_acquired_date = Utility.date_formatter(ics_info[11],0)
        self.ics_obj.cmb_acquired_month.set(new_acquired_date[0])
        self.ics_obj.cmb_acquired_day.set(new_acquired_date[1])
        self.ics_obj.cmb_acquired_year.set(new_acquired_date[2])

        self.ics_obj.ent_useful_life_var.set(ics_info[12])


    def stateUI(self,controller):
        if controller == 0:
            self.ics_obj.ent_ics_no.configure(state="readonly")
            self.ics_obj.ent_iar_no.configure(state="readonly")
            self.ics_obj.cmb_ics_office.configure(state="disabled")
            self.ics_obj.cmb_ics_month.configure(state="disabled")
            self.ics_obj.cmb_ics_day.configure(state="disabled")
            self.ics_obj.cmb_ics_year.configure(state="disabled")

            self.ics_obj.ent_article.configure(state="readonly")
            self.ics_obj.spn_quantity.configure(state="readonly")
            self.ics_obj.ent_unit.configure(state="readonly")
            self.ics_obj.txt_description.configure(state="disable")
            self.ics_obj.ent_amount.configure(state="readonly")
            self.ics_obj.cmb_acquired_month.configure(state="disabled")
            self.ics_obj.cmb_acquired_day.configure(state="disabled")
            self.ics_obj.cmb_acquired_year.configure(state="disabled")
            self.ics_obj.ent_useful_life.configure(state="readonly")

            self.ics_obj.btn_save_ics.configure(text="Edit",command=self.callback_edit)

        elif controller == 2:
            self.ics_obj.ent_ics_no.configure(state="normal")
            self.ics_obj.ent_iar_no.configure(state="normal")
            self.ics_obj.cmb_ics_office.configure(state="readonly")
            self.ics_obj.cmb_ics_month.configure(state="readonly")
            self.ics_obj.cmb_ics_day.configure(state="readonly")
            self.ics_obj.cmb_ics_year.configure(state="readonly")

            self.ics_obj.ent_article.configure(state="normal")
            self.ics_obj.spn_quantity.configure(state="normal")
            self.ics_obj.ent_unit.configure(state="normal")
            self.ics_obj.txt_description.configure(state="normal")
            self.ics_obj.ent_amount.configure(state="normal")
            self.ics_obj.cmb_acquired_month.configure(state="readonly")
            self.ics_obj.cmb_acquired_day.configure(state="readonly")
            self.ics_obj.cmb_acquired_year.configure(state="readonly")
            self.ics_obj.ent_useful_life.configure(state="normal")

    ''' ================================= Callback Methods ============================================= '''

    def callback_edit(self):
        self.stateUI(2)
        self.ics_obj.btn_save_ics.configure(text="Save",command=self.callback_save)

    def callback_save(self):
        confirmation_answer = messagebox.askyesno("Edit Confirmation","Are you sure you want to save eddited information?")
        if confirmation_answer is True:
            try:
                dict_item_ics = {
                    "item_id": self.item_id,
                    "ics_no": self.ics_obj.ent_ics_no_var.get(),
                    "iar_no": self.ics_obj.ent_iar_no_var.get(),
                    "ics_scan": os.getcwd() + f'\\scans\\scan_ics\\{self.ics_obj.ent_ics_no_var.get()}',
                    "iar_scan": os.getcwd() + f'\\scans\\scan_iar\\{self.ics_obj.ent_iar_no_var.get()}',
                    "office": self.ics_obj.cmb_ics_office.get(),
                    "date": Utility.date_formatter(datetime.datetime(int(self.ics_obj.cmb_ics_year.get()),self.dict_month[self.ics_obj.cmb_ics_month.get()],int(self.ics_obj.cmb_ics_day.get())),1),
                    "article": self.ics_obj.ent_article_var.get(),
                    "quantity": self.ics_obj.spn_quantity_var.get(),
                    "unit": self.ics_obj.ent_unit_var.get(),
                    "description": self.ics_obj.txt_description.get("1.0","end-1c"),
                    "amount": self.ics_obj.ent_amount_var.get(),
                    "date_acquired": Utility.date_formatter(datetime.datetime(int(self.ics_obj.cmb_acquired_year.get()),self.dict_month[self.ics_obj.cmb_acquired_month.get()],int(self.ics_obj.cmb_acquired_day.get())),1),
                    "durability": self.ics_obj.ent_useful_life_var.get()
                }
            except Exception as e:
                messagebox.showerror("Error occured","Error: ",e)
            else:
                try:
                    self.db_obj.edit_item(dict_item_ics)
                    Utility.create_directory(dict_item_ics["ics_scan"])
                    Utility.transfer_files(self.old_ics_directory,dict_item_ics["ics_scan"])
                    Utility.create_directory(dict_item_ics["iar_scan"])
                    Utility.transfer_files(self.old_iar_directory, dict_item_ics["iar_scan"])
                except Exception as e:
                    print(e)
                else:
                    messagebox.showinfo("Edit Success","Editted information has been saved to database")



    def callback_delete(self):
        self.db_obj.delete_item(self.item_id)
        self.parent.destroy()

    ''' ================================= Static Methods ============================================= '''


class ICS_insert:
    ics_image_status = False
    iar_image_status = False
    def __init__(self,parent):
        self.parent = parent
        self.parent.grab_set()
        self.ics_obj = ICS(self.parent)
        self.db_obj = Database()
        self.initUI()

    def initUI(self):
        self.ics_obj.btn_scan_ics.configure(text="ICS scan", command=lambda: self.save_scan(0))
        self.ics_obj.btn_scan_iar.configure(text="IAR scan", command=lambda: self.save_scan(1))
        self.ics_obj.btn_save_ics.configure(text="Saveeee",command=self.callback_save_ics)




    ''' ================================= callback ============================================= '''

    def save_scan(self,controller):
        '''
            controller = 0 = ics_image
            controller = 1 = iar_image
        '''

        if controller == 0:
            if self.ics_obj.ent_ics_no_var.get() is "":
                messagebox.showerror("Empty ICS Number","Please enter ics number before uploading the scanned documents")
            else:
                try:
                    scan_ics_dir = os.getcwd() + f'\\scans\\scan_ics\\{self.ics_obj.ent_ics_no_var.get()}'
                    os.makedirs(scan_ics_dir)
                except FileExistsError:
                    pass
                finally:
                    os.startfile(scan_ics_dir)
                    self.ics_image_status = True


        elif controller == 1:
            if self.ics_obj.ent_iar_no_var.get() is "":
                messagebox.showerror("Empty IAR Number","Please enter ics number before uploading the scanned documents")
            else:
                try:
                    scan_iar_dir = os.getcwd() + f'\\scans\\scan_iar\\{self.ics_obj.ent_iar_no_var.get()}'
                    os.makedirs(scan_iar_dir)
                except FileExistsError:
                    pass
                finally:
                    os.startfile(scan_iar_dir)
                    self.iar_image_status = True

    def callback_save_ics(self):
        if self.ics_image_status is True and self.iar_image_status is True:
            try:
                dict_ics_info = {
                    'ics_no': self.ics_obj.ent_ics_no_var.get(),
                    'iar_no': self.ics_obj.ent_iar_no_var.get(),
                    'ics_scan': os.getcwd() + f'\\scans\\scan_ics\\{self.ics_obj.ent_ics_no_var.get()}',
                    'iar_scan': os.getcwd() + f'\\scans\\scan_iar\\{self.ics_obj.ent_iar_no_var.get()}',
                    'ics_office': self.ics_obj.cmb_ics_office.get(),
                    'ics_date':  datetime.datetime(int(self.ics_obj.cmb_ics_year.get()),self.ics_obj.dict_month[self.ics_obj.cmb_ics_month.get()],int(self.ics_obj.cmb_ics_day.get())).strftime("%Y-%m-%d")
                }

                for key in dict_ics_info.keys():
                    if dict_ics_info[key] is "" or len(self.ics_obj.tree_ics_item.get_children()) == 0:
                        raise TypeError


                ics_id = self.db_obj.save_ics(dict_ics_info)
                print(ics_id)
            except TypeError:
                messagebox.showerror("Incomplete Fields","Please Complete All The Fields")
            except KeyError:
                messagebox.showerror("Date Error","Please Fix The ICS Date")
            except Exception as e:
                messagebox.showerror("Unexpected Error","An Unexpected Error Occured.\n"
                                                        "Please Double Check The Fields")
            else:
               try:
                    '''
                        [0] = ics_id
                        [0] = quantity
                        [1] = unit
                        [2] = article
                        [3] = description
                        [4] = amount
                        [5] = date_acquired
                        [6] = est useful life
                    '''
                    list_tree_children = []
                    for child in self.ics_obj.tree_ics_item.get_children():
                        list_temp_1 = []
                        list_temp_1.append(ics_id)
                        for item in self.ics_obj.tree_ics_item.item(child)['values']:
                            list_temp_1.append(item)
                        list_tree_children.append(list_temp_1)
                    print(list_tree_children)
                    self.db_obj.save_item_ics(list_tree_children)
               except Exception as e:
                    messagebox.showerror("Error Occured","Error: ",e)
               else:
                    messagebox.showinfo("New Value Inserted","New ICS has been successfully inserted to database")
                    self.parent.destroy()

        elif self.ics_image_status is False:
            messagebox.showerror("No Image Uploaded","Please Upload image before saving")


