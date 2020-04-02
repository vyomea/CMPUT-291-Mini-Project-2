import parser
from datetime import datetime

class Info:

    def __init__(self, query, cursors, output_type):
        
        self.parser = parser
        
        self.reviews_cursor = cursors[0]
        self.scores_cursor = cursors[1]
        self.pterms_cursor = cursors[2]
        self.rterms_cursor = cursors[3]

        self.output_type = output_type


        #Query details
        self.score_low, self.score_high = parser.scoreparser(query)
        self.pterm = None
        self.rterm = None
        self.terms = set()

        self.term_dict = parser.keywordsParser(query)

        # Assuming there is only one pterm and rterm
        for word in self.term_dict:
            if self.term_dict[word] == (True, False):
                self.pterm = word
            
            elif self.term_dict[word] == (False, True):
                self.rterm = word
            
            elif self.term_dict[word] == (False, False):
                self.terms.add(word)

        self.date_low, self.date_high = parser.dateparser(query)

        self.price_low, self.price_high = parser.priceparser(query)
    
    def execute_query(self):

        matches = set()
        product_title = None

        if self.pterm:

            if self.pterm[-1] != "%":
                result = self.pterms_cursor.set_range(self.pterm.encode("utf-8"))
                
                while result != None:
                    product_title = result[0].decode("utf-8").lower()
                    review_id = int(result[1].decode("utf-8"))

                    if self.pterm == product_title:
                        matches.add(review_id)

                    result = self.pterms_cursor.next()
                
            else:
                self.pterm = self.pterm[:-1]
                result = self.pterms_cursor.set_range(self.pterm.encode("utf-8"))

                while result != None:
                    if result[0].decode("utf-8").startswith(self.pterm):
                        matches.add(int(result[1].decode("utf-8")))
                    
                    result = self.pterms_cursor.next()

            if len(matches) == 0:
                    print("No matches found!")

                    return

        matches_2 = set()
        if self.rterm:
            if self.rterm[-1] != "%":
                result = self.rterms_cursor.set_range(self.rterm.encode("utf-8"))

                while result != None:
                    review_summ_text = result[0].decode("utf-8")
                    review_id = int(result[1].decode("utf-8"))

                    if self.rterm == review_summ_text:
                        if self.pterm:
                            matches_2.add(review_id)
                        else:
                            matches_2.add(review_id)
                            matches.add(review_id)


                    result = self.rterms_cursor.next()
            
            else:
                self.rterm = self.rterm[:-1]
                result = self.rterms_cursor.set_range(self.rterm.encode("utf-8"))

                while result != None:
                    if result[0].decode("utf-8").startswith(self.rterm):
                        if self.pterm:
                            matches_2.add(int(result[1].decode("utf-8")))
                        else:
                            matches_2.add(int(result[1].decode("utf-8")))
                            matches.add(int(result[1].decode("utf-8")))
                        
                    result = self.rterms_cursor.next()

            matches = matches.intersection(matches_2)

            if len(matches) == 0:
                print("No matches found!")

                return 

        #terms
        if len(self.terms) > 0:
            for term in self.terms:
                if term[-1] != "%":
                    result = self.pterms_cursor.set_range(term.encode("utf-8"))
                    
                    while result != None:
                        product_title = result[0].decode("utf-8").lower()
                        review_id = int(result[1].decode("utf-8"))

                        if term == product_title:
                            matches.add(review_id)

                        result = self.pterms_cursor.next()
                    

                    result = self.rterms_cursor.set_range(term.encode("utf-8"))

                    while result != None:
                        review_summ_text = result[0].decode("utf-8")
                        review_id = int(result[1].decode("utf-8"))

                        if term == review_summ_text:
                            if self.pterm:
                                matches_2.add(review_id)
                            else:
                                matches_2.add(review_id)
                                matches.add(review_id)


                        result = self.rterms_cursor.next()
                    
                else:
                    term = term[:-1]
                    result = self.pterms_cursor.set_range(term.encode("utf-8"))

                    while result != None:
                        if result[0].decode("utf-8").startswith(term):
                            matches.add(int(result[1].decode("utf-8")))
                        
                        result = self.pterms_cursor.next()

                    result = self.rterms_cursor.set_range(term.encode("utf-8"))

                    while result != None:
                        if result[0].decode("utf-8").startswith(term):
                            if self.pterm:
                                matches_2.add(int(result[1].decode("utf-8")))
                            else:
                                matches_2.add(int(result[1].decode("utf-8")))
                                matches.add(int(result[1].decode("utf-8")))
                            
                        result = self.rterms_cursor.next()

            matches = matches.intersection(matches_2)



        matches_2 = set()
        # score
        if self.score_low or self.score_high:
            if not self.score_low:
                score_low_n = 0.0
            else:
                score_low_n = self.score_low

            if not self.score_high:
                score_high_n = 5.0
            else:
                score_high_n = self.score_high

            result = self.scores_cursor.set_range("{}".format(score_low_n).encode("utf-8"))
            # result[0] = review score, result[1] = review ID

            while result != None:
                review_score = float(result[0].decode("utf-8"))
                review_id = int(result[1].decode("utf-8"))
                
                if review_score > float(score_low_n) and review_score < float(score_high_n):
            
                    if not (self.pterm or self.rterm):
                        matches.add(review_id)
                        matches_2.add(review_id)
                    else:
                        matches_2.add(review_id)
                
                result = self.scores_cursor.next()

            matches = matches.intersection(matches_2)


        #price

        price_low_n = None
        price_high_n = None
        if (len(matches) > 0) and not (self.price_low == None or self.price_high == None):
            if self.price_low == None:
                price_low_n = 0.0
            else:
                price_low_n = self.price_low

            if self.price_high == None:
                price_high_n = float("inf")
            else:
                price_high_n = self.price_high

            to_remove = []
            for match in matches:
                result = self.reviews_cursor.set("{}".format(match).encode("utf-8"))
                price = self.get_price(result)

                if price == "unknown" or not (float(price) > price_low_n and float(price) < price_high_n):
                    to_remove.append(match)

            for element in to_remove:
                matches.remove(element)

        #date
        if (len(matches) > 0) and not (self.date_low == None or self.date_high == None):

            to_remove = []
            for match in matches:
                result = self.reviews_cursor.set("{}".format(match).encode("utf-8"))
                date = self.get_date(result) #timestamp
                date_obj = datetime.fromtimestamp(date)

                date_high_tp = datetime.timestamp(datetime.strptime(self.date_high,'%Y/%m/%d'))
                date_obj_high = datetime.fromtimestamp(date_high_tp)

                date_low_tp = datetime.timestamp(datetime.strptime(self.date_low,'%Y/%m/%d'))
                date_obj_low = datetime.fromtimestamp(date_low_tp)

                if self.date_low:
                    if self.date_high:

                        if date_obj >= date_obj_high:
                            to_remove.append(match)

                    if date_obj <= date_obj_low:
                        to_remove.append(match)  

            for element in to_remove:
                matches.remove(element)

        if len(matches) > 0:
            if self.output_type == "brief":
                self.get_data_brief(matches)
            else:
                self.get_data_full(matches)
        else:
            print("No matches found!")


    def get_date(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]
        user_id_start = s2.index('"')
        s3 = s2[user_id_start + 1:]
        user_id_end = s3.index('"')
        s4 = s3[user_id_end + 1:]

        record_value_stripped = s4.split(",")
        date = record_value_stripped[3]

        return int(date)
    
    def get_price(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]
    
        record_value_stripped =  s2.split(",")
        price = record_value_stripped[1]

        return price
    
    def get_score(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]
        user_id_start = s2.index('"')
        s3 = s2[user_id_start + 1:]
        user_id_end = s3.index('"')
        s4 = s3[user_id_end + 1:]

        record_value_stripped = s4.split(",")
        score = record_value_stripped[2]

        return score

    def get_user_id(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]

        record_value_stripped = s2.split(",")
        user_id = record_value_stripped[2]

        return user_id
    
    def get_profile_name(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]

        record_value_stripped = s2.split(",")
        profile_name = record_value_stripped[3]

        return profile_name

    def get_helpfulness(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]

        record_value_stripped = s2.split(",")
        helpfulness = record_value_stripped[4]

        return helpfulness
    
    def get_timestamp(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]

        record_value_stripped = s2.split(",")
        timestamp = record_value_stripped[6]

        return timestamp


    def get_product_title(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_start:p_title_end]

        product_title = s2

        return product_title

    def get_review_summary(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index("\"")
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]

        record_value_stripped = s2.split(",")
        review_summary = record_value_stripped[7]
        char = ''

        while char != '"':
            for i in range(8, 11):
                if char == '"':
                    break
                for j in range(len(record_value_stripped[i])):
                    if record_value_stripped[i][j] == '"':
                        char = '"'
                        break
                    else:
                        review_summary += record_value_stripped[i][j]
        review_summary += '"'

        return review_summary

    def get_review_full(self, record):
        record_value = record[1].decode("utf-8")
        p_title_start = record_value.index('"')
        s = record_value[p_title_start + 1:]
        p_title_end = s.index('"')
        s2 = s[p_title_end + 1:]
        profile_name_start = s2.index('"')
        s3 = s2[profile_name_start + 1:]
        profile_name_end = s3.index('"')
        s4 = s3[profile_name_end + 1:]
        review_summary_start = s4.index('"')
        s5 = s4[review_summary_start + 1:]
        review_summary_end = s5.index('"')

        review_full = s5[review_summary_end + 1:]

        return review_full





    def get_data_brief(self, matches):

        for match in matches:
            res = self.reviews_cursor.set("{}".format(match).encode("utf-8"))
            review_id = int(res[0].decode("utf-8"))
            record_value = res[1].decode("utf-8").split(",")
            product_title = record_value[1]
            review_score = self.get_score(res)
            
            print("-"*50)
            print("Review ID: {}".format(review_id))
            print("Product Title: {}".format(product_title))
            print("Review Score: {}".format(review_score))
            print()

    def get_data_full(self, matches):

        for match in matches:
            res = self.reviews_cursor.set("{}".format(match).encode("utf-8"))
            review_id = int(res[0].decode("utf-8"))
            record_value = res[1].decode("utf-8").split(",")
            product_id = record_value[0]
            product_title = self.get_product_title(res)
            product_price = self.get_price(res)
            user_id = self.get_user_id(res)
            profile_name = self.get_profile_name(res)
            helpfulness = self.get_helpfulness(res)
            review_score = self.get_score(res)
            review_timestamp = self.get_timestamp(res)
            review_summary = self.get_review_summary(res)
            review_full_text = self.get_review_full(res)
            
            print("-"*50)
            print("Review ID: {}".format(review_id))
            print("Product ID: {}".format(product_id))
            print("Product Title: {}".format(product_title))
            print("Product Price: {}".format(product_price))
            print("User ID: {}".format(user_id))
            print("Profile name: {}".format(profile_name))
            print("Helpfulness: {}".format(helpfulness))
            print("Review Score: {}".format(review_score))
            print("Review Timestamp: {}".format(review_timestamp))
            print("Review Summary: {}".format(review_summary))
            print("Review Full: {}".format(review_full_text))

            print()










        

    

