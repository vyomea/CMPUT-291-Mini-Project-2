from connection import Connection
from info import Info

def main():
    output_type = "brief" # default

    #Print the welcome message:
    print("Welcome to this searcher!")
    print("To quit, please enter ::quit")

    conn = Connection()
    conn.connect()
    cursors = conn.get_cursors()

    parser = None

    info = Info(parser, cursors, output_type)

    quit = False

    while not quit:
        query = input("(Searcher)>>> ").lower()

        if query == "::quit":
            print("Thank you for using our service")
            conn.close()
            break

        elif query == "output=breif":
            output_type = "brief"
        
        elif query == "output=full":
            output_type = "full"

        else:
            info.execute_score()



if __name__ == "__main__":
    main()
