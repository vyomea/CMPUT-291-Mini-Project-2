class Info:

    def __init__(self, parser, cursors, output_type):
        
        self.parser = parser

        self.reviews_cursor = cursors[0]
        self.scores_cursor = cursors[1]
        self.pterms_cursor = cursors[2]
        self.rterms_cursor = cursors[3]

        self.output_type = output_type

    def execute_score(self):
        """
        Execute the score query
        scores.txt: (review score, review id)
        """
        score_low = 0
        score_high = 5

        result = self.scores_cursor.set_range("{}".format(score_low).encode("utf-8")) # result[0] = review score, result[1] = review ID    

        matches = set()

        if result != None:
            while result != None and int(result[0].decode("utf-8")) <= score_high:
                print(result[0].decode("utf-8") + ", ", end="")
                print(result[1].decode("utf-8"))
                result = self.scores_cursor.next()






        

    

