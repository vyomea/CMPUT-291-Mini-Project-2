import parser

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
        
        self.modFlag, self.ptermFlag, self.pterm, self.rtermFlag, self.rterm = parser.termParser(query)

        #self.date_low, self.date_high = parser.dateparser(query)

       # self.price_low, self.price_high = parser.priceparser(query)
    
    def execute_term(self):

        exists = True

        matches = set()
        other_term = None

        if self.ptermFlag:
            result = self.pterms_cursor.set_range(self.pterm.encode("utf-8"))

            while result != None:
                product_title = result[0].decode("utf-8").split()[0]

                if len(result) > 1:
                    other_term = result[0].decode("utf-8").split()[1]
                review_id = int(result[1].decode("utf-8"))

                if self.pterm == product_title:
                    matches.add(review_id)

                result = self.pterms_cursor.next()
            
            if len(matches) == 0:
                exists = False
        
        num = len(matches)
        
        if self.rtermFlag:
            result = self.rterms_cursor.set_range(self.rterm.encode("utf-8"))

            while result != None:
                product_title = result[0].decode("utf-8").split()[0]
                
                if len(result) > 1:
                    other_term = result[0].decode("utf-8").split()[1]
                review_id = int(result[1].decode("utf-8"))

                if self.rterm == product_title:
                    matches.add(review_id)

                result = self.rterms_cursor.next()
            
            if len(matches) == num:
                exists = False


        if exists:
            self.get_data(matches)

        

    def execute_score(self):
        """
        Execute the score query
        scores.txt: (review score, review id)
        """

        exists = True
        result = self.scores_cursor.set_range("{}".format(self.score_low).encode("utf-8"))
         # result[0] = review score, result[1] = review ID    

        matches = set()

        if result != None:
            while result != None and int(result[0].decode("utf-8")) <= self.score_high:
                review_id = result[1].decode("utf-8")
                review_score = result[0].decode("utf-8")

                if self.ptermFlag:
                    review_id_pterm = self.pterms_cursor.set_range(self.pterm.encode("utf-8"))[0]

                    if review_id_pterm != review_id:
                        exists = False

                if self.rtermFlag:
                    review_id_rterm = self.rterms_cursor.set_range(self.pterm.encode("utf-8"))[0]

                    if review_id_rterm != review_id:
                        exists = False




                result = self.scores_cursor.next()

    def get_data(self, matches):

        for match in matches:
            res = self.reviews_cursor.set("{}".format(match).encode("utf-8"))
            print(len(res))
            review_id = int(res[0].decode("utf-8"))
            product_id = res[1].decode("utf-8")
            # product_title = res[2].decode("utf-8")
            # product_price = res[3].decode("utf-8")
            # user_id = res[4].decode("utf-8")
            # profile_name = res[5].decode("utf-8")
            # helpfulness = res[6].decode("utf-8")
            # review_score = res[7].decode("utf-8")
            # review_timestamp = res[8].decode("utf-8")
            # review_summary = res[9].decode("utf-8")
            # review_full_text = res[10].decode("utf-8")

            print("Review ID: {} Product ID: {}".format(review_id, product_id))









        

    

