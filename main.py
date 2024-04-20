import SQL_Injection_V1
import xss
import openport

FileName = input("Enter the input filename: ")

while True:
    x = input(
        "Enter what do you want to test ?\n1. cross-site scripting \n2. SQL injection \n3. Port scanning\n4. Exit\n"
    )

    if x == "1":
        # Get the URL input
        with open(FileName, "r") as file:
            url = [url.strip() for url in file.readlines()]
            url = "".join(url)
            url = url[0:-1]
            print(url)
        # url = input("Enter the URL of the website to scan for XSS vulnerabilities: ")

        # Run the code from file1
        xss.main(url)

    elif x == "2":
        with open(FileName, "r") as file:
            url = file.read().strip()

        SQL_Injection_V1.main(url)

    elif x == "3":
        with open(FileName, "r") as file:
            url = file.read().strip()

        openport.main(url)

    elif x == "4":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please try again.")
