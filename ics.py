import os
import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext
from tkinter import filedialog
from tkinter import ttk
import locale

from templates.utility import Utility
from templates.database import Database
from templates.tabFrameTemplate import TabFrameTemplate


class ICS:
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
        ttk.Label(frame1, text="Acc. Person", style="ICS.TLabel").grid(row=2,column=0,sticky="nsew")
        self.ent_acc_person_var = tk.StringVar()
        self.ent_acc_person = ttk.Entry(frame1, textvariable=self.ent_acc_person_var)

        self.ent_acc_person.grid(row=2,column=1,columnspan=2,sticky="nsew")

        # ========== END: Row 2 ========== #
        # ========== START: Row 3 ========== #
        ttk.Label(frame1, text="Office", style="ICS.TLabel").grid(row=3, column=0, sticky="nsew")
        self.cmb_ics_office = ttk.Combobox(frame1, state="readonly", values=self.db_obj.get_offices())

        self.cmb_ics_office.grid(row=3, column=1, columnspan=2, sticky="nsew")
        # ========== END: Row 3 ========== #
        # ========== START: Row 4 ========== #
        ttk.Label(frame1,text="Date",style="ICS.TLabel").grid(row=4,column=0,sticky="nsew")
        date_frame = ttk.Frame(frame1,style="ICS.TFrame")

        self.cmb_ics_month = ttk.Combobox(date_frame,state="readonly", values=list(Utility.month_dictionary(0)))
        self.cmb_ics_day = ttk.Combobox(date_frame,state="readonly", values=Utility.days_generator())
        self.cmb_ics_year = ttk.Combobox(date_frame,state="readonly", values=Utility.years_generator())

        self.cmb_ics_month.grid(row=0, column=0,sticky="nsew")
        self.cmb_ics_day.grid(row=0, column=1,sticky="nsew")
        self.cmb_ics_year.grid(row=0, column=2,sticky="nsew")

        date_frame.grid(row=4,column=1,sticky="nsew")
        for widget in date_frame.winfo_children():
            widget.grid_configure(padx=10,pady=10)

        # ========== END: Row 4 ========== #


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
        self.cmb_acquired_month = ttk.Combobox(items_date_frame, state="readonly", values=[ x for x in Utility.month_dictionary(0)])
        self.cmb_acquired_day = ttk.Combobox(items_date_frame, state="readonly", values=Utility.days_generator())
        self.cmb_acquired_year = ttk.Combobox(items_date_frame, state="readonly", values=Utility.years_generator())
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
        try:
            # self.items variable will save all the information per item
            self.items = {
                'quantity': float(self.spn_quantity.get().strip()),
                'unit': self.ent_unit.get().strip(),
                'article': self.ent_article.get().strip(),
                'description': self.txt_description.get("1.0","end-1c"),
                'amount': float(self.ent_amount.get().strip()),
                'acquisition': datetime.datetime(int(self.cmb_acquired_year.get()),Utility.month_dictionary(1,self.cmb_acquired_month.get()),int(self.cmb_acquired_day.get())),
                'durability': self.ent_useful_life.get()
            }
        # In case an error occured. Highlight the ACQUISITION DATE
        except Exception as e:
            tk.messagebox.showerror("Error Occured!","Please Complete All Fields")
        # If there are no errors occured during fetching of data
        else:
            # Converting acquisition format from yyyy-mm-d to yyyy-mm-dd
            self.items['acquisition'] = Utility.date_formatter(self.items['acquisition'], 1)

            # Convert dictionary's values to list
            line = list(self.items.values())

            # Show the values in the item Treeview
            self.tree_ics_item.insert('', tk.END, values=line)

            # If inserting is success, values in the fields will be removed
            self.callback_clear_item()


    def callback_delete_item(self):
        try:
            # Get the current selected items in the tree
            selected_item = (self.tree_ics_item.focus())

            # Delete the selected items from the tree
            self.tree_ics_item.delete(selected_item)

        # In case an error occurs
        # This error will show when the delete button was pressed and there is no item selected in the tree
        except:
            messagebox.showerror("Selection Error","Please select an item to be deleted")


class ICS_edit:
    def __init__(self, parent, item_id):
        self.parent = parent
        self.parent.grab_set()
        self.item_id = item_id
        self.db_obj = Database()
        self.ics_obj = ICS(self.parent)

        self.initUI()
        self.load_information()
        self.stateUI(0)

    def initUI(self):

        # Removes the Treeview in the Window
        self.ics_obj.tree_ics_item.destroy()

        # Removes the add button in the window
        self.ics_obj.btn_add_item.destroy()

        # Removes the delete button in the window
        self.ics_obj.btn_delete_item.destroy()

        # Removes the clear button in the window
        self.ics_obj.btn_clear_item.destroy()

        # Add delete button in the window
        self.btn_delete = ttk.Button(self.ics_obj.frame3,text="Delete Item",command=self.callback_delete)

        self.btn_delete.grid(row=0,column=1,sticky="nsew")

    def load_information(self):
        '''
            [0] = ics_no
            [1] = iar_no
            [2] = ics_scan
            [3] = iar_scan
            [5] = accountable_person
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
        # ---------- Assigning and Displaying the current information ---------- #

        # Get item information based on item id
        dict_ics_info = self.db_obj.get_ics(self.item_id)



        # Assign ics number to ent_ics_no_var
        self.ics_obj.ent_ics_no_var.set(dict_ics_info["ics_no"])

        # Assign iar number to ent_iar_no_var
        self.ics_obj.ent_iar_no_var.set(dict_ics_info["iar_no"])

        # Assign the directory of ics
        self.ics_directory = dict_ics_info["ics_scan"]

        # Assign the directory of iar
        self.iar_directory = dict_ics_info["iar_scan"]

        # Assign the accountable person
        self.ics_obj.ent_acc_person_var.set(dict_ics_info["accountable_person"])

        # Assign and Display the office description
        self.ics_obj.cmb_ics_office.set(dict_ics_info["office_description"])

        # Assign the ics date to new date. This is an object
        new_date = Utility.date_formatter(dict_ics_info["ics_date"], 0)

        # Assign and Display the article
        self.ics_obj.ent_article_var.set(dict_ics_info["article"])

        # Assign and Display the quantity
        self.ics_obj.spn_quantity_var.set(dict_ics_info["quantity"])

        # Assign and Display the unit
        self.ics_obj.ent_unit_var.set(dict_ics_info["unit"])

        # Assign and Display the description
        self.ics_obj.txt_description.insert(tk.END, dict_ics_info["description"])

        # Assign and Display amount
        self.ics_obj.ent_amount_var.set(dict_ics_info["amount"])

        # Assign date acquired. This is an object
        new_acquired_date = Utility.date_formatter(dict_ics_info["date_acquired"], 0)

        # Assign and Display durability
        self.ics_obj.ent_useful_life_var.set(dict_ics_info["durability"])

        # ---------- Scan Button Configuration ---------- #
        # This will assign the address of btn_scan_ics based on ics_info[2]
        result_ics = self.ics_obj.btn_scan_ics.configure(command=lambda: Utility.open_directory(self.ics_directory))
        # This will assign the address of btn_scan_iar based on ics_info[3]
        result_iar = self.ics_obj.btn_scan_iar.configure(command=lambda: Utility.open_directory(self.iar_directory))



        # ----------  ICS Date Configuration   ---------- #
        # This will display the ICS Date month based on info[5]
        self.ics_obj.cmb_ics_month.set(new_date[0])
        # This will display the ICS Date day based on info[5]
        self.ics_obj.cmb_ics_day.set(new_date[1])
        # This will display the ICS Date year based on info[5]
        self.ics_obj.cmb_ics_year.set(new_date[2])

        # ---------- Date Acquired Configuration ---------- #
        # This will display the Date Acquired month based on info[11]
        self.ics_obj.cmb_acquired_month.set(new_acquired_date[0])
        # This will display the Date acquired day based on info[11]
        self.ics_obj.cmb_acquired_day.set(new_acquired_date[1])
        # This will display the Date acquired year based on info[11]
        self.ics_obj.cmb_acquired_year.set(new_acquired_date[2])


    def stateUI(self,controller):
        '''
        Controller
            [0] = Disable/Readonly
            [1] = Edittable

        :param controller:
        :return:
        '''
        if controller == 0:
            self.ics_obj.ent_ics_no.configure(state="readonly")
            self.ics_obj.ent_iar_no.configure(state="readonly")
            self.ics_obj.ent_acc_person.configure(state="readonly")
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
            self.ics_obj.ent_acc_person.configure(state="normal")
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
    def callback_ics_dir(self):
        new_ics_dir = filedialog.askdirectory()
        Utility.create_directory(new_ics_dir + f"\\{self.ics_obj.ent_ics_no_var.get()}")

    def callback_iar_dir(self):
        new_iar_dir = filedialog.askdirectory()
        Utility.create_directory(new_iar_dir + f"\\{self.ics_obj.ent_iar_no_var.get()}")


    def callback_edit(self):
        self.ics_obj.btn_scan_ics.configure(text="Make ICS dir", command=self.callback_ics_dir)
        self.ics_obj.btn_scan_iar.configure(text="Make IAR dir", command=self.callback_iar_dir)

        # This will change the file from disable/readonly to editable or normal state
        self.stateUI(2)
        # Configuring the save button
        self.ics_obj.btn_save_ics.configure(text="Save",command=self.callback_save)

    def callback_save(self):
        # Confirmation popup. [True = Continue Saving][False = Cancel Saving]
        confirmation_answer = messagebox.askyesno("Edit Confirmation","Are you sure you want to save editted information?")
        # Checks if answer is "YES"
        if confirmation_answer is True:
            try:
                # If the ICS No. or IAR No. is empty, error will occur
                # This is needed before creating ICS or IAR folder
                if self.ics_obj.ent_ics_no_var.get() == "" or self.ics_obj.ent_iar_no_var.get() == "":
                    raise ValueError

                dict_item_ics = {
                    "item_id": self.item_id,
                    "ics_no": self.ics_obj.ent_ics_no_var.get(),
                    "iar_no": self.ics_obj.ent_iar_no_var.get(),
                    "ics_scan": self.ics_directory.rsplit('\\',1)[0] + f"\\{self.ics_obj.ent_ics_no_var.get()}",
                    "iar_scan": self.iar_directory.rsplit('\\',1)[0] + f"\\{self.ics_obj.ent_iar_no_var.get()}",
                    "accountable_person": self.ics_obj.ent_acc_person_var.get(),
                    "office": self.ics_obj.cmb_ics_office.get(),
                    "date": Utility.date_formatter(datetime.datetime(int(self.ics_obj.cmb_ics_year.get()),
                                                                     Utility.month_dictionary(1,self.ics_obj.cmb_ics_month.get()),
                                                                     int(self.ics_obj.cmb_ics_day.get())),1),
                    "article": self.ics_obj.ent_article_var.get(),
                    "quantity": self.ics_obj.spn_quantity_var.get(),
                    "unit": self.ics_obj.ent_unit_var.get(),
                    "description": self.ics_obj.txt_description.get("1.0","end-1c"),
                    "amount": self.ics_obj.ent_amount_var.get(),
                    "date_acquired": Utility.date_formatter(datetime.datetime(int(self.ics_obj.cmb_acquired_year.get()),
                                                                              Utility.month_dictionary(1,self.ics_obj.cmb_acquired_month.get()),
                                                                              int(self.ics_obj.cmb_acquired_day.get())),1),
                    "durability": self.ics_obj.ent_useful_life_var.get()
                }

                # Save edits
                self.db_obj.edit_item(dict_item_ics)

                # If the new ics does not have a directory yet, it will create a new one
                Utility.create_directory(self.ics_directory.rsplit('\\',1)[0] + f"\\{self.ics_obj.ent_ics_no_var.get()}")

                # If the new iar does not have a directory yet, it will create a new one
                Utility.create_directory(self.iar_directory.rsplit('\\',1)[0] + f"\\{self.ics_obj.ent_iar_no_var.get()}")

                # # Transfer files from old ics directory to new directory
                # Utility.transfer_files(self.ics_directory, self.)
                #
                # # Transfer files from old iar directory to new directory
                # Utility.transfer_files(self.iar_directory,
                #                        os.getcwd() + f'\\scans\\scan_iar\\{self.ics_obj.ent_iar_no_var.get()}')

            # Raised if ICS no field and IAR no field is empty
            except ValueError as e:
                messagebox.showerror("ERROR","ICS Number and IAR Number must not be empty")

            # Raised in case an unepected error occurs
            except Exception as e:
                messagebox.showerror("Error occured",f"Error {e}")

            # If no error occured
            else:
                # Confirmation pop up will show
                messagebox.showinfo("Edit Success","Editted information has been saved to database")
                # close edit window
                self.parent.destroy()

    def callback_delete(self):
        # Deletion of item confirmation
        confirmation = messagebox.askyesno("Delete Confirmation","Are you sure you want to delete this item?")
        # If the user confirms, the item will be deleted
        if confirmation is True:
            # Delete the item for item_ics table using item id
            result = self.db_obj.delete_item(self.item_id)
            # result = 0 if an error occured while saving to database
            if result == 0:
                # Pop up message informing user about saving failed
                messagebox.showerror("ERROR","An unexpected database error occured")
            # result = 1 if database saving succeed
            elif result == 1:
                # Pop up message informing user about the success
                messagebox.showinfo("Success","Item Successfully Deleted")
            # Close the window
            self.parent.destroy()

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
        # Configure button functionalities
        # self.ics_obj.ent_ics_no.bind("<FocusOut>",self.event_ics_directory)
        # self.ics_obj.ent_iar_no.bind("<FocusOut>",self.event_iar_directory)
        self.ics_obj.btn_scan_ics.configure(text="Make ICS Dir", command=lambda: self.callback_save_scan(0))
        self.ics_obj.btn_scan_iar.configure(text="Make IAR Dir", command=lambda: self.callback_save_scan(1))
        self.ics_obj.btn_save_ics.configure(text="Save",command=self.callback_save_ics)

    ''' ================================= Events ============================================= '''

    # def event_ics_directory(self, event=None):
    #     ics_number = self.ics_obj.ent_ics_no_var.get()
    #     if ics_number == "":
    #         self.ics_image_status = False
    #         messagebox.showerror("ERROR","Please enter an ICS Number.")
    #     else:
    #         ics_directory = filedialog.askdirectory()
    #         ics_directory = ics_directory + f"\\{ics_number}"
    #         Utility.create_directory(ics_directory)
    #         Utility.open_directory(ics_directory)
    #         self.ics_image_status = True
    #
    # def event_iar_directory(self, event=None):
    #     iar_number = self.ics_obj.ent_iar_no_var.get()
    #     if iar_number == "":
    #         messagebox.showerror("ERROR","Please enter an IAR Number.")
    #         self.ics_image_status = False
    #     else:
    #         iar_directory = filedialog.askdirectory()
    #         iar_directory = iar_directory + f"\\{iar_number}"
    #         Utility.create_directory(iar_directory)
    #         Utility.open_directory(iar_directory)
    #         self.iar_image_status = True
    ''' ================================= callback ============================================= '''

    def callback_save_scan(self, controller):
        '''
            controller = 0 = ics_image
            controller = 1 = iar_image
        '''

        # Checks if there is an ICS No. inputted in ics_no entry
        if controller == 0:
            self.ics_number = self.ics_obj.ent_ics_no_var.get().strip()
            # If ICS No. entry is empty
            if self.ics_number == "":
                messagebox.showerror("Empty ICS Number","Please enter ics number before uploading the scanned documents")
            # If ICS No. entry is NOT empty
            else:
                try:
                    # Assign the ICS folder location to a variable
                    scan_ics_dir = filedialog.askdirectory(parent = self.parent,initialdir="C:\\Users\\Public\\Documents")
                    # If directory is not yet existing, it will create a new one
                    if scan_ics_dir == "":
                        messagebox.showinfo("INFO","You have entered empty directory")
                    else:
                        self.final_scan_ics_dir = scan_ics_dir + f"\\{self.ics_number.strip()}"
                        Utility.create_directory((self.final_scan_ics_dir))
                # If an error occured why creating a directory
                except Exception as e:
                    messagebox.showerror("ERROR",e)
                # IF directory assignment and directory creation is successful
                else:
                    # Open the directory, in order for the user to save the files
                    os.startfile(self.final_scan_ics_dir)
                    # Used as an indication that the directory has been created
                    self.ics_image_status = True

        # Checks if there is an IAR No. inputted in iar_no entry
        elif controller == 1:
            self.iar_number = self.ics_obj.ent_iar_no_var.get().strip()
            # If IAR No. entry is empty
            if self.iar_number is "":
                messagebox.showerror("Empty IAR Number","Please enter ics number before uploading the scanned documents")
            # If IAR No. entry is NOT empty
            else:
                try:
                    # Assign the IAR folder location to a variable
                    scan_iar_dir = filedialog.askdirectory()
                    self.final_scan_iar_dir = scan_iar_dir + f"\\{self.iar_number}"
                    # If directory is not yet existing, it will create a new one
                    Utility.create_directory((self.final_scan_iar_dir.strip()))
                except Exception as e:
                    messagebox.showerror("ERROR",e)
                else:
                    # Open the directory, in order for the user to save the files
                    os.startfile(self.final_scan_iar_dir)
                    # Used as an indication that the directory has been created
                    self.iar_image_status = True

    def callback_save_ics(self):
        # Get the ICS date
        ics_month = self.ics_obj.cmb_ics_month.get().strip()
        ics_day = self.ics_obj.cmb_ics_day.get().strip()
        ics_year = self.ics_obj.cmb_ics_year.get().strip()

        # If there are no items
        if len(self.ics_obj.tree_ics_item.get_children()) == 0:
            messagebox.showerror("ERROR","Please add at least 1 item in the list")
        # If ICS date is empty
        elif ics_month == "" or ics_day == "" or ics_year == "":
            messagebox.showerror("ERROR","Please fill all the dates")
        # If image not yet set
        elif self.ics_image_status is False or self.iar_image_status is False:
            messagebox.showerror("ERROR","No image uploaded, please upload ICS and IAR scan")
        else:
            dict_ics_info = {
                'ics_no': self.ics_obj.ent_ics_no_var.get().strip(),
                'iar_no': self.ics_obj.ent_iar_no_var.get().strip(),
                'ics_scan': self.final_scan_ics_dir.strip(),
                'iar_scan': self.final_scan_iar_dir.strip(),
                'accountable_person': self.ics_obj.ent_acc_person_var.get().strip(),
                'ics_office': self.ics_obj.cmb_ics_office.get().strip(),
                'ics_date': Utility.date_formatter(datetime.datetime(int(ics_year),
                                                                     Utility.month_dictionary(1,ics_month),
                                                                     int(ics_day)),1)
            }

            empty_field = False
            for key in dict_ics_info.keys():
                # If there are some empty fields or if the item is empty
                if dict_ics_info[key] == "":
                    empty_field = True
                    break

            if empty_field is True:
                messagebox.showerror("ERROR","Please fill all the fields")
            else:
                ics_id = self.db_obj.save_ics(dict_ics_info)
                if ics_id == -1:
                    messagebox.showerror("ERROR","An error occured while saving the ics information. Sequence 1")
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



