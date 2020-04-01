def main():
    output_brief = False
    output_full = False

    #Print the welcome message:
    print("Welcome to this searcher!")
    print("To quit, please enter :quit")

    quit = False

    while not quit:
        query = input(">>> ").lower()

        if query == "QUIT":
            print("Thank you for using our service")

        elif query == "output=breif":
            output_brief = True
        
        elif query == "output=full":
            output_full = True

        else:
            pass



if __name__ == "__main__":
    main()
