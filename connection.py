from bsddb3 import db

class Connection:
    
    def __init__(self):
        """
        Initialize the databases and setflags
        """

        # Intitialize the db
        self.reviews_db = db.DB()
        self.scores_db = db.DB()
        self.pterms_db = db.DB()
        self.rterms_db = db.DB()

        # Set flags
        self.reviews_db.set_flags(db.DB_DUP)
        self.scores_db.set_flags(db.DB_DUP)
        self.pterms_db.set_flags(db.DB_DUP)
        self.rterms_db.set_flags(db.DB_DUP)

    def connect(self):
        """
        Connect to the databases and get the cursors
        """

        # Open the connections
        self.reviews_db.open("rw.idx", None, db.DB_HASH, db.DB_CREATE)
        self.scores_db.open("sc.idx", None, db.DB_BTREE, db.DB_CREATE)
        self.pterms_db.open("pt.idx", None, db.DB_BTREE, db.DB_CREATE)
        self.rterms_db.open("rt.idx", None, db.DB_BTREE, db.DB_CREATE)

        # Get the cursors
        self.reviews_cursor = self.reviews_db.cursor()
        self.scores_cursor = self.scores_db.cursor()
        self.pterms_cursor = self.pterms_db.cursor()
        self.rterms_cursor = self.rterms_db.cursor()
    
    def close(self):
        """
        Close the connection to the curosors and databases
        """

        # Close the cursors
        self.reviews_cursor.close()
        self.scores_cursor.close()
        self.pterms_cursor.close()
        self.rterms_cursor.close()

        # Close the connection to the databases
        self.reviews_db.close()
        self.scores_db.close()
        self.pterms_db.close()
        self.rterms_db.close()

    
    




        
