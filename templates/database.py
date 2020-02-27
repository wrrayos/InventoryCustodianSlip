import mysql.connector
import traceback

class Database:
    def __init__(self):
        try:
            self.mydb = mysql.connector.connect(
                host = "localhost",
                user = "root",
                passwd = "admin123",
                database = "ics"
            )

            self.curr = self.mydb.cursor()
            self.get_offices()
        except Exception as e:
            print(e)

    def get_offices(self):
        try:
            query = "SELECT office_desc FROM offices"
            self.curr.execute(query)
            result = self.curr.fetchall()
            list_offices = [x[0] for x in result]
            list_offices.sort()
        except Exception as e:
            print(e)
        else:
            return list_offices

    '''
    ********************** ICS **************************
    '''
    def get_ics(self, item_id):
        try:
            query = "SELECT ics.ics_no, ics.iar_no, ics.ics_scan_add, ics.iar_scan_add,ics.accountable_person, offices.office_desc, ics.ics_date, " \
                    "item_ics.article, item_ics.description, item_ics.qty, item_ics.unit, item_ics.amount, item_ics.date_acquired, item_ics.est_life " \
                    "FROM ics " \
                    "INNER JOIN offices " \
                    "ON ics.office_id = offices.office_id " \
                    "INNER JOIN item_ics " \
                    "ON ics.ics_id = item_ics.ics_id " \
                    "WHERE item_ics.id = %s "

            val = item_id

            self.curr.execute(query,(val,))

            result_ics_info = self.curr.fetchall()

        except Exception as e:
            print(e)
        else:
            list_temp = ["ics_no", "iar_no", "ics_scan", "iar_scan", "accountable_person",
                         "office_description", "ics_date", "article", "description", "quantity",
                         "unit", "amount", "date_acquired", "durability"]
            zip_obj = zip(list_temp,result_ics_info[0])
            dict_ics_info = dict(zip_obj)
            return dict_ics_info



    def get_ics_items(self):
        try:
            query="SELECT * FROM report"

            self.curr.execute(query,)
            result = self.curr.fetchall()
        except Exception as e:
            print(e)
        else:
            self.mydb.commit()
            return result

    def get_ics_report(self,item_ids):
        try:
            query = "SELECT ICS_Number, IAR_Number, Office, ICS_Date, Article, Description, Quantity, Unit, Amount, Date_Acquired," \
                    "Estimated_Useful_Life FROM final_report WHERE id = %s"
            self.curr.execute(query,(item_ids,))
            result = self.curr.fetchone()
            # result = [list(x) for x in result]
        except Exception as e:
            print(e)
        else:
            return result


    def save_ics(self,dict_ics={}):
        '''
            ics_no
            iar_no
            ics_scan
            iar_scan
            ics_office
            ics_date

        :param dict_ics:
        :return:
        '''
        try:
            # Check if ICS No. already exists
            query = "SELECT EXISTS (SELECT ics_id FROM ics WHERE ics_no = %s)"
            val = dict_ics['ics_no']
            self.curr.execute(query, (val,))
        except Exception as e:
            print(e)
        else:
            result = self.curr.fetchone()
            # If ICS No. does not exists
            if result[0] == 0:
                try:
                    query = "SELECT office_id FROM offices WHERE office_desc = %s"
                    val = dict_ics['ics_office']
                    self.curr.execute(query, (val,))

                    office_id_tuple = self.curr.fetchone()
                    office_id = office_id_tuple[0]

                    query = "INSERT INTO ics (ics_no,iar_no,ics_scan_add,iar_scan_add,accountable_person,office_id,ics_date) " \
                            "VALUES (%s,%s,%s,%s,%s,%s,%s)"

                    val = (dict_ics['ics_no'],
                           dict_ics['iar_no'],
                           dict_ics['ics_scan'],
                           dict_ics['iar_scan'],
                           dict_ics['accountable_person'],
                           office_id,
                           dict_ics['ics_date'])

                    print(dict_ics['ics_no'])
                    print(dict_ics['iar_no'])
                    print(dict_ics['ics_scan'])
                    print(dict_ics['iar_scan'])
                    print(dict_ics['accountable_person'])
                    print(dict_ics['ics_date'])

                    self.curr.execute(query, val)
                except Exception as e:
                    traceback.print_exc()
                    self.mydb.rollback()
                    return -1
                else:
                    self.mydb.commit()
                try:
                    query = "SELECT ics_id FROM ics WHERE ics_id = (SELECT LAST_INSERT_ID())"
                    self.curr.execute(query)

                    result = self.curr.fetchone()
                except Exception as e:
                    print("Error in getting last ID: ", e)
                else:
                    self.mydb.commit()
                    return result[0]
            else:
                query = "SELECT ics_id FROM ics WHERE ics_no = %s"
                val = dict_ics['ics_no']

                self.curr.execute(query,(val,))
                result = self.curr.fetchone()

                return result[0]



    def save_item_ics(self, values=[]):
        val = values
        tuple_val = [tuple(i) for i in val]

        try:
            query = 'INSERT INTO item_ics (ics_id,qty,unit,article,description,amount,date_acquired,est_life) ' \
                    'VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'

            '''
                [0] = ics_id
                [1] = quantity
                [2] = unit
                [3] = article
                [4] = description
                [5] = amount
                [6] = date_acquired
                [7] = durability
                
            '''
            self.curr.executemany(query,tuple_val)
        except Exception as e:
            self.mydb.rollback()
        else:
            self.mydb.commit()

    def delete_item(self,item_id):
        try:
            query = "DELETE FROM item_ics WHERE id = %s"
            val = item_id
            self.curr.execute(query,(val,))
        except Exception as e:
            return 0
        else:
            self.mydb.commit()
            return 1
        finally:
            self.curr.close()
            self.mydb.close()

    def edit_item(self, item_new_info):
        '''
            item_new_info['item_id']
            item_new_info['ics_no']
            item_new_info['iar_no']
            item_new_info['ics_scan']
            item_new_info['iar_scan']
            item_new_info['accountable_person']
            item_new_info['office']
            item_new_info['date']
            item_new_info['article']
            item_new_info['quantity']
            item_new_info['unit']
            item_new_info['description']
            item_new_info['amount']
            item_new_info['date_acquired']
            item_new_info['durability']
        :param item_new_info:
        :return:
        '''

        # Getting ics_id of an item using the item's id
        try:
            # Get ics_id of an item using item_id
            query = "SELECT ics_id FROM item_ics WHERE id = %s"
            val = item_new_info['item_id']

            self.curr.execute(query,(val,))

            ics_id = self.curr.fetchone()
            # ics_id variable holds the ics_id of the item to be editted
            # This ics_id purpose is to hold the new ics_id of the item
            ics_id = ics_id[0]

            # This will update the item_ics table, which consist of items information
            query = "UPDATE item_ics SET " \
                    "article = %s," \
                    " description = %s," \
                    " qty = %s, unit = %s," \
                    " amount = %s," \
                    " date_acquired = %s," \
                    " est_life = %s " \
                    "WHERE id = %s"

            self.curr.execute(query, (item_new_info['article'],
                                      item_new_info['description'],
                                      item_new_info['quantity'],
                                      item_new_info['unit'],
                                      item_new_info['amount'],
                                      item_new_info['date_acquired'],
                                      item_new_info['durability'],
                                      item_new_info['item_id']))


            # This will get the office_id of an item using office_description of the delected item
            query = "SELECT office_id FROM offices WHERE office_desc = %s"
            self.curr.execute(query, (item_new_info['office'],))
            office_id = self.curr.fetchone()

            # office_id variable will hold the office_id
            office_id = office_id[0]
            print(office_id)


            # This will update the ics table in the database, which holds the secondary information of the items
            query = "UPDATE ics " \
                    "SET " \
                    "ics_no = %s, " \
                    "iar_no = %s, " \
                    "ics_scan_add = %s, " \
                    "iar_scan_add = %s, " \
                    "accountable_person = %s, " \
                    "office_id = %s, " \
                    "ics_date = %s " \
                    "WHERE ics_id = %s"

            self.curr.execute(query,
                              (item_new_info['ics_no'],
                               item_new_info['iar_no'],
                               item_new_info['ics_scan'],
                               item_new_info['iar_scan'],
                               item_new_info['accountable_person'],
                               office_id,
                               item_new_info['date'],
                               ics_id))

        except Exception as e:
            print(traceback.print_exc())
            self.mydb.rollback()
        else:
            self.mydb.commit()

    def search_items(self,controller,value):
        val = value
        if controller == 0:
            try:
                self.curr.callproc("search_via_accountable_person",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        if controller == 1:
            try:
                self.curr.callproc("search_via_ics_number",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 2:
            try:
                self.curr.callproc("search_via_iar_number",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 3:
            try:
                self.curr.callproc("search_via_office_desc",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 4:
            try:
                self.curr.callproc("search_via_ics_date",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 5:
            try:
                self.curr.callproc("search_via_item_article",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 6:
            try:
                self.curr.callproc("search_via_item_quantity",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 7:
            try:
                self.curr.callproc("search_via_item_unit",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 8:
            try:
                self.curr.callproc("search_via_item_amount",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 9:
            try:
                self.curr.callproc("search_via_date_acquired",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items


    def filter_items(self,dict_information):

        try:
            self.curr.callproc("filter_items",(dict_information['office'],
                                               dict_information['ics_date_from'],
                                               dict_information['ics_date_to'],
                                               dict_information['article'],
                                               dict_information['quantity'],
                                               dict_information['unit'],
                                               dict_information['amount'],
                                               dict_information['date_acquired_from'],
                                               dict_information['date_acquired_to'],
                                               dict_information['durability'],))
            result = self.curr.stored_results()
            for content in result:
                items = content.fetchall()
        except Exception as e:
            print(e)
        else:
            return items



                



