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

        self.date_low, self.date_high = parser.dateparser(query)

        #self.price_low, self.price_high = parser.priceparser(query)
    
    def execute_term(self):

        exists = True

        matches = set()
        other_term = None
        product_title = None

        print("THIS: {}".format(self.pterm))
        

        if self.ptermFlag:
            self.pterm = self.pterm.split()[0]
            result = self.pterms_cursor.set_range(self.pterm.encode("utf-8"))
            

            while result != None:
                product_title = result[0].decode("utf-8").lower()
                

                # if len(result) > 1:
                #     other_term = result[0].decode("utf-8").split()[1]
                review_id = int(result[1].decode("utf-8"))

                if self.pterm == product_title:
                    matches.add(review_id)

                result = self.pterms_cursor.next()
            
            if len(matches) == 0:
                exists = False
                print("NOO")

                return # TODO
        
        num = len(matches)

        matches_2 = set()
        print("RTERM: {}".format(self.rterm))
        if self.rtermFlag:
            self.rterm = self.rterm.split()[0]
            result = self.rterms_cursor.set_range(self.rterm.encode("utf-8"))

            while result != None:
                review_summ_text = result[0].decode("utf-8")
                
                # if len(result) > 1:
                #     other_term = result[0].decode("utf-8").split()[1]
                review_id = int(result[1].decode("utf-8"))

                if self.rterm == review_summ_text:
                    if self.ptermFlag:
                        matches_2.add(review_id)
                    else:
                        matches_2.add(review_id)
                        matches.add(review_id)


                result = self.rterms_cursor.next()
            
            matches = matches.intersection(matches_2)

            if len(matches) == 0:
                exists = False
                print("NOO2")

                return # TODO
        
        num = len(matches)


        matches_2 = set()
        # score
        print("HIII")
        print(self.score_low, self.score_high)
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
            print("SCORE: {}".format( float(result[0].decode("utf-8"))))

            while result != None:
                review_score = float(result[0].decode("utf-8"))
                review_id = int(result[1].decode("utf-8"))
                
                if review_score > float(score_low_n) and review_score < float(score_high_n):
            
                    if not (self.ptermFlag or self.rtermFlag):
                        matches.add(review_id)
                        matches_2.add(review_id)
                    else:
                        matches_2.add(review_id)
                
                result = self.scores_cursor.next()

            matches = matches.intersection(matches_2)
        print(len(matches_2))
        print("Hello")
        print(len(matches))


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









        

    

