
def mainmenu():
    """Display menu and get a valid choice."""
    print("CAESAR CIPHER MESSAGING")
    print("-----------------------")
    print("1. Start a message")
    print("2. Read and reply to a message")
    print("3. Quit")
    loop = True
    while loop != False:
        try:
            user = int(input("Enter your choice: "))
            if user not in [1,2,3]:
                raise ValueError("Out of range. (1 to 3)")
            else:
                loop = False
        except ValueError:
            print("ValueError - Must be a number answer (1-3)")
    return user

def getAlphabet():
    """Get a valid alphabet from the user."""
    while True:
        alphabet = input("Enter supported characters: ")
        if not alphabet:
            print("Alphabet cannot be empty.")
        elif len(set(alphabet)) != len(alphabet):
            print("Alphabet cannot contain duplicates.")
        else:
            return alphabet
 
 
def getShift():
    """Get an integer shift from the user."""
    while True:
        try:
            return int(input("Enter shift: "))
        except ValueError:
            print("Please enter an integer.")
 
 
def encrypt(message, alphabet, shift):
    """Encrypt or decrypt a message using a Caesar cipher."""
    result = ""
    for char in message:
        if char in alphabet:
            index = alphabet.index(char)
            new_index = (index + shift) % len(alphabet)
            result += alphabet[new_index]
        else:
            result += char
    return result
 
 
def createMessage():
    """Create a new conversation file."""
    alphabet = getAlphabet()
    shift = getShift()
    while True:
        message = input("Enter message: ")
        if message.strip():
            break
        print("Message cannot be empty.")
    encrypted = encrypt(message, alphabet, shift)
    filename = input("Enter filename: ")
    if not filename.endswith(".txt"):
        filename += ".txt"
    try:
        with open(filename, "x") as file:
            file.write(alphabet + "\n")
            file.write(str(shift) + "\n")
            file.write(encrypted + "\n")
    except FileExistsError:
        confirm = input("File exists. Overwrite? (y/n): ")
        if confirm.lower() == "y":
            with open(filename, "w") as file:
                file.write(alphabet + "\n")
                file.write(str(shift) + "\n")
                file.write(encrypted + "\n")
        else:
            print("File not overwritten.")
            return
    print("Encrypted message:", encrypted)
    print("Message saved to", filename)
 
 
def readMessages():
    """Read and decrypt all messages in a conversation."""
    while True:
        filename = input("Enter filename (M for main menu): ")
        if filename.lower() == "m":
            return
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
            alphabet = lines[0].strip()
            shift = int(lines[1].strip())
            if not alphabet or len(set(alphabet)) != len(alphabet):
                raise ValueError
            if len(lines) < 3:
                raise ValueError
            break
        except FileNotFoundError:
            print("File", filename, "was not found.")
        except (ValueError, IndexError):
            print("Invalid conversation file.")
            return
    print("\nMESSAGES\n--------")
    for number, line in enumerate(lines[2:], 1):
        message = encrypt(line.strip(), alphabet, -shift)
        print(f"{number}. {message}")
    replyToMessage(filename, alphabet, shift)
 
 
def replyToMessage(filename, alphabet, shift):
    """Encrypt and append a reply to a conversation."""
    print("\nSupported characters:")
    print(alphabet)
    while True:
        reply = input("Enter your reply: ")
        if reply.strip():
            break
        print("Reply cannot be empty.")
    encrypted = encrypt(reply, alphabet, shift)
    print("Encrypted message:", encrypted)
    try:
        with open(filename, "a") as file:
            file.write(encrypted + "\n")
        print("Message saved to", filename)
    except OSError:
        print("Could not save reply.")
 
 
def main():
    """Run the Caesar cipher messaging program."""
    while True:
        choice = mainmenu()
        if choice == 1:
            createMessage()
        elif choice == 2:
            readMessages()
        elif choice == 3:
            print("Goodbye!")
            break
 
 
if __name__ == "__main__":
    main()