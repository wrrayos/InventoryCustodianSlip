import mysql.connector
import datetime

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
    def get_ics(self,row_contents):
        print(row_contents)
        try:
            query = "SELECT ics.ics_no, ics.iar_no, ics.ics_scan_add, ics.iar_scan_add, offices.office_desc, ics.ics_date, " \
                    "item_ics.article, item_ics.description, item_ics.qty, item_ics.unit, item_ics.amount, item_ics.date_acquired, item_ics.est_life " \
                    "FROM ics " \
                    "INNER JOIN offices " \
                    "ON ics.office_id = offices.office_id " \
                    "INNER JOIN item_ics " \
                    "ON ics.ics_id = item_ics.ics_id " \
                    "WHERE item_ics.id = %s "

            val = row_contents

            self.curr.execute(query,(val,))

            result_ics_info = self.curr.fetchall()

            return result_ics_info[0]

        except Exception as e:
            print(e)

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

    def get_ics_report(self):
        try:
            query = "SELECT * FROM final_report"
            self.curr.execute(query,)
            result = self.curr.fetchall()
            result = [list(x) for x in result]
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
            query = "SELECT office_id FROM offices WHERE office_desc = %s"
            val = dict_ics['ics_office']
            self.curr.execute(query, (val,))

            office_id_tuple = self.curr.fetchone()
            office_id = office_id_tuple[0]

        except Exception as e:
            print("office problem ",e)
        else:
            try:
                query = "INSERT INTO ics (ics_no,iar_no,ics_scan_add,iar_scan_add,office_id,ics_date) VALUES (%s,%s,%s,%s,%s,%s)"
                val = (dict_ics['ics_no'],
                       dict_ics['iar_no'],
                       dict_ics['ics_scan'],
                       dict_ics['iar_scan'],
                       office_id,
                       dict_ics['ics_date'])

                self.curr.execute(query,val)

                self.mydb.commit()

            except Exception as e:
                print("Proglem in ics-contents ",e)
            else:
                try:
                    query = "SELECT ics_id FROM ics WHERE ics_id = (SELECT LAST_INSERT_ID())"
                    self.curr.execute(query)

                    result = self.curr.fetchone()
                except Exception as e:
                    print("Error in getting last ID: ",e)
                else:
                    self.mydb.commit()

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
            self.mydb.commit()

        except Exception as e:
            print(e)

    def delete_item(self,item_id):
        try:
            query = "DELETE FROM item_ics WHERE id = %s"
            val = item_id
            self.curr.execute(query,(val,))
        except Exception as e:
            print(e)
        else:
            self.mydb.commit()
        finally:
            self.curr.close()
            self.mydb.close()

    def edit_item(self,item_info):
        # Getting ics_id of an item
        try:
            query = "SELECT ics_id FROM item_ics WHERE id = %s"
            val = item_info['item_id']

            self.curr.execute(query,(val,))

            ics_id = self.curr.fetchone()
            ics_id = ics_id[0]
        except Exception as e:
            print("Error in ics_id: ",e)
        else:
            try:
                query = "UPDATE item_ics SET " \
                        "article = %s, description = %s, qty = %s, unit = %s, amount = %s, date_acquired = %s, est_life = %s " \
                        "WHERE id = %s"
                self.curr.execute(query,(item_info['article'],item_info['description'],item_info['quantity'],item_info['unit'],
                                         item_info['amount'],item_info['date_acquired'],item_info['durability'],item_info['item_id']))
            except Exception as e:
                print("Error in update_item: ",e)
            else:
                self.mydb.commit()
                try:
                    query = "SELECT office_id FROM offices WHERE office_desc = %s"
                    self.curr.execute(query,(item_info['office'],))
                    office_id = self.curr.fetchone()
                    office_id = office_id[0]
                except Exception as e:
                    print("Error in office: ",e)
                else:
                    try:
                        query = "UPDATE ics SET " \
                                "ics_no = %s, iar_no = %s, ics_scan_add = %s, iar_scan_add = %s, office_id = %s, ics_date = %s " \
                                "WHERE ics_id = %s"
                        self.curr.execute(query,(item_info['ics_no'],item_info['iar_no'],item_info['ics_scan'],item_info['iar_scan'],
                                                 office_id, item_info['date'],ics_id))
                    except Exception as e:
                        print("Error in ics: ",e)
                    else:
                        self.mydb.commit()

    def search_items(self,controller,value):
        val = value
        if controller == 0:
            try:
                self.curr.callproc("search_via_ics_number",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 1:
            try:
                self.curr.callproc("search_via_iar_number",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 2:
            try:
                self.curr.callproc("search_via_office_desc",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 3:
            try:
                self.curr.callproc("search_via_ics_date",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 4:
            try:
                self.curr.callproc("search_via_item_article",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 5:
            try:
                self.curr.callproc("search_via_item_quantity",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 6:
            try:
                self.curr.callproc("search_via_item_unit",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items
        elif controller == 7:
            try:
                self.curr.callproc("search_via_item_amount",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items

        elif controller == 8:
            try:
                self.curr.callproc("search_via_date_acquired",(val,))
                result = self.curr.stored_results()
                for content in result:
                    items = content.fetchall()
            except Exception as e:
                print(e)
            else:
                return items






                



