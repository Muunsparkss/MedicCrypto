from bitstring import BitArray
from PIL import Image
#Defining the XOR enryption and decryption function.We are going to use this in Id encryption.
lenghtofname= 0
lenghtofsurname=0
def xor_encrypt_decrypt(text, key):
    encrypted_text = ""
    
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))
    
    return encrypted_text
DOCTOR_INFO = {
    "ahmed abeideh": "D5377",
    "mehmet sedat": "D6663",
    "john doe": "D1002",
    "mahmoud abdelkafi": "D5173",
    "oznur sengel": "D1004"
}
def get_doctor_id(doctor_name):
    """Retrieves the doctor ID based on the doctor's name."""
    doctor_id = DOCTOR_INFO.get(doctor_name.lower())
    if not doctor_id:
        raise ValueError(f"Doctor name '{doctor_name}' not found in DOCTOR_INFO.")
    return doctor_id

def encrypt():
    verify = 0
    #Image opening from our file
    while verify==0:
        try:
            file_path=input("\nEnter the path of the image with its extension:\t")
            input_image = Image.open(file_path)
            verify = 1
        except:
            print("ERROR : Couldnt find the image. Try entering again! \n")
    verify =0
    #Loading the pixel map so that we can change the pixels
    pixel_map = input_image.load() 
    #Getting the information from The Doctor
    while verify==0:
        try:
            doctor_name = input("\n\nPlease enter doctor's name:\t")
            doc_id = get_doctor_id(doctor_name)
            verify=1
        except:
            print("ERROR : Couldn't find doctor name. Try again... \n")
    verify=0
    id_num = input("\nPlease enter patient's identification number(exmp-> 34156744985):\t")
    while len(id_num)!=11:
        print("Please enter a valid identification number.(11 digits)\n")
        id_num = input("\nPlease enter patient's identification number(exmp-> 34156744985):\t")    
       
    name = input("\nPlease enter patient's name:\t")
    while len(name)>25:
        print("ERROR : Name is too long. (max 25 characters)")
        name = input("\nPlease enter patient's name:\t")

    surname = input("\nPlease enter patient's surname:\t")
    while len(surname)>25:
        print("ERROR : Surname is too long. (max 25 characters)")
        surname = input("\nPlease enter patient's surname:\t")

    ins_num = input ("\nPlease enter patient's insurance number(exmp-> I433156):\t")
    while ((len(ins_num)!=7) | (ins_num.startswith("I")==0))==1:
        if len(ins_num)!=7 :
            print("ERROR (Invalid Lenght) : Enter a valid insurance number.")
        if ins_num.startswith("I")!=1:
            print("ERROR (Invalid form): The number should start with I.")
        ins_num = input ("\nPlease enter patient's insurance number(exmp-> I433156):\t")
    
    given_date = input("\nPlease enter the date of inspection(MMDDYYYY):\t")    
    while len(given_date)!=8:
        print("ERROR : Please enter a valid format.\n")
        given_date = input("\nPlease enter the date of inspection(MMDDYYYY):\t")

    #Id Encryption: We have used XOR encryption for this part.Each digit is encrypted by the doctor's id(we use it as the key).
    id_encrypted = xor_encrypt_decrypt(id_num,doc_id)
    name_encrypted = xor_encrypt_decrypt(name,doc_id)
    surname_encrypted = xor_encrypt_decrypt(surname,doc_id)
    ins_num_encrypted = xor_encrypt_decrypt(ins_num,doc_id)
    given_date_encrypted = xor_encrypt_decrypt(given_date,doc_id)
    #After encryption, we encode the cipher text to binary
    byte_array_id= id_encrypted.encode('utf-8', errors='replace')
    byte_array_name= name_encrypted.encode('utf-8', errors='replace')
    byte_array_surname= surname_encrypted.encode('utf-8', errors='replace')
    byte_array_ins= ins_num_encrypted.encode('utf-8', errors='replace')
    byte_array_date= given_date_encrypted.encode('utf-8', errors='replace')
    #We turn the encoded bytes to integer values
    binary_int_id=int.from_bytes(byte_array_id,"big")
    binary_int_name=int.from_bytes(byte_array_name,"big")
    binary_int_surname=int.from_bytes(byte_array_surname,"big")
    binary_int_ins=int.from_bytes(byte_array_ins,"big")
    binary_int_date=int.from_bytes(byte_array_date,"big")
    #Then We convert them to binary with the bin() function
    binary_string_id=bin(binary_int_id)
    binary_string_name=bin(binary_int_name)
    binary_string_surname=bin(binary_int_surname)
    binary_string_ins=bin(binary_int_ins)
    binary_string_date=bin(binary_int_date)
    #After encoding, we change the pixel values of spesific positions in the pixel matrix of our image 
    #Each for loop is for one information embedding
    #But first we need to embedd the lenghts of the bytes for the decoding part.Otherwise our code won't be flexible.
    pixel_map[511,198]=(1,1,len(byte_array_id))
    pixel_map[511,199]=(1,1,len(byte_array_name))
    pixel_map[511,200]=(1,1,len(byte_array_surname))
    pixel_map[511,201]=(1,1,len(byte_array_ins))
    pixel_map[511,202]=(1,1,len(byte_array_date))
    global lenghtofname
    lenghtofname=len(binary_string_name)
    global lenghtofsurname
    lenghtofsurname=len(binary_string_surname)
    pixel_map[150,1]=(1,lenghtofname,lenghtofsurname)

    #Now for the Embedding of the information
    
    for i in range(len(binary_string_id)):
        if binary_string_id[i] =='1':
            pixel_map[2,2+i]=(6,6,6)
        if binary_string_id[i]=='b':
            pixel_map[2,2+i]=(4,4,4)
        if binary_string_id[i]=='0':
            pixel_map[2,2+i]=(2,2,2)

    for i in range(len(binary_string_name)):
        if i <=490:
            if binary_string_name[i] =='1':
                pixel_map[3,511-i]=(6,6,6)
            if binary_string_name[i]=='b':
                pixel_map[3,511-i]=(4,4,4)
            if binary_string_name[i]=='0':
                pixel_map[3,511-i]=(2,2,2)
        if i >490:
            if binary_string_name[i] =='1':
                pixel_map[5,511-i]=(6,6,6)
            if binary_string_name[i]=='b':
                pixel_map[5,511-i]=(4,4,4)
            if binary_string_name[i]=='0':
                pixel_map[5,511-i]=(2,2,2)

    for i in range(len(binary_string_surname)):
        if i<=490:
            if binary_string_surname[i] =='1':
                pixel_map[4,511-i]=(6,6,6)
            if binary_string_surname[i]=='b':
                pixel_map[4,511-i]=(4,4,4)
            if binary_string_surname[i]=='0':
                pixel_map[4,511-i]=(2,2,2)
        if i>490:
            if binary_string_surname[i] =='1':
                pixel_map[4,511-i]=(6,6,6)
            if binary_string_surname[i]=='b':
                pixel_map[4,511-i]=(4,4,4)
            if binary_string_surname[i]=='0':
                pixel_map[4,511-i]=(2,2,2)

    for i in range(len(binary_string_ins)):
        if binary_string_ins[i] =='1':
            pixel_map[509,2+i]=(6,6,6)
        if binary_string_ins[i]=='b':
            pixel_map[509,2+i]=(4,4,4)
        if binary_string_ins[i]=='0':
            pixel_map[509,2+i]=(2,2,2)

    for i in range(len(binary_string_date)):
        if binary_string_date[i] =='1':
            pixel_map[509,511-i]=(6,6,6)
        if binary_string_date[i]=='b':
            pixel_map[509,511-i]=(4,4,4)
        if binary_string_date[i]=='0':
            pixel_map[509,511-i]=(2,2,2)
    
    
    
    #We save the encrypted file and show it to the doctor and the patient.
    output_name = input("Enter the output file name: ")
    input_image.save(str(output_name)+".png", format="png")
    print("Output image saved")
    input_image.show()
def decrypt():
    # Getting the path of the image
    file_path = input("\n\nEnter the path of the image with its extension:\t")
    doctor_name = input("\n\nPlease enter doctor's name:\t")
    doc_id = get_doctor_id(doctor_name)
    # Image opening from our file
    input_image = Image.open(file_path)
    # Loading the pixel map so that we can change the pixels
    pixel_map = input_image.load()
    # Initializing the strings
    binary_string_id = ''
    binary_string_name = ''
    binary_string_surname = ''
    binary_string_ins = ''
    binary_string_date = ''
    pixel_map[1,1]=(6,6,6)
    # We are assigning the pixel values of 0, 1 and b in order to understand and fetch the data from our encrypted image.
    pixel_one = pixel_map[1, 1]  # The RGB for 1's in the binary is (6,6,6)
    pixel_bin = pixel_map[2, 3]  # The RGB for b in the binary is (4,4,4)
    pixel_zero = pixel_map[2, 2]  # The RGB for 0's in the binary is (2,2,2)

    # Getting the encoded byte lengths from the B value of RGB from our selected pixels.
    # This step is important because if we don't take the length of the bytes, we won't be able to decode our information.
    _, _, b, _,= pixel_map[511, 198]
    _, _, b1, _,= pixel_map[511, 199]
    _, _, b2, _,= pixel_map[511, 200]
    _, _, b3, _,= pixel_map[511, 201]
    _, _, b4, _,= pixel_map[511, 202]
    _, lsname, lname, _, =pixel_map[150,1]
    # Fetching the binary data from the embedded pixels
    for i in range(0, 89):
        if pixel_map[2, 2 + i] == pixel_one:
            binary_string_id += '1'
        elif pixel_map[2, 2 + i] == pixel_bin:
            binary_string_id += 'b'
        elif pixel_map[2, 2 + i] == pixel_zero:
            binary_string_id += '0'

    for i in range(lname*2):
        if i <=490:
            if pixel_map[3, 511 - i] == pixel_one:
                binary_string_name += '1'
            elif pixel_map[3, 511 - i] == pixel_bin:
                binary_string_name += 'b'
            elif pixel_map[3, 511 - i] == pixel_zero:
                binary_string_name += '0'
        if i>490:
            if pixel_map[5, 511 - i] == pixel_one:
                binary_string_name += '1'
            elif pixel_map[5, 511 - i] == pixel_bin:
                binary_string_name += 'b'
            elif pixel_map[5, 511 - i] == pixel_zero:
                binary_string_name += '0'

    for i in range(lsname*2):
        if i<=490:
            if pixel_map[4, 511 - i] == pixel_one:
                binary_string_surname += '1'
            elif pixel_map[4, 511 - i] == pixel_bin:
                binary_string_surname += 'b'
            elif pixel_map[4, 511 - i] == pixel_zero:
                binary_string_surname += '0'
        if i>490:
            if pixel_map[6, 511 - i] == pixel_one:
                binary_string_surname += '1'
            elif pixel_map[6, 511 - i] == pixel_bin:
                binary_string_surname += 'b'
            elif pixel_map[6, 511 - i] == pixel_zero:
                binary_string_surname += '0'


    for i in range(0, 89):
        if pixel_map[509, 2 + i] == pixel_one:
            binary_string_ins += '1'
        elif pixel_map[509, 2 + i] == pixel_bin:
            binary_string_ins += 'b'
        elif pixel_map[509, 2 + i] == pixel_zero:
            binary_string_ins += '0'

    for i in range(0, 89):
        if pixel_map[509, 511 - i] == pixel_one:
            binary_string_date += '1'
        elif pixel_map[509, 511 - i] == pixel_bin:
            binary_string_date += 'b'
        elif pixel_map[509, 511 - i] == pixel_zero:
            binary_string_date += '0'

    # Turning binary strings that we fetched into integer values
    int_id = int(binary_string_id, 2)
    int_name = int(binary_string_name, 2)
    int_surname = int(binary_string_surname, 2)
    int_ins = int(binary_string_ins, 2)
    int_date = int(binary_string_date, 2)

    # Packing out integer values into bytes using the byte lengths that we have also fetched from the image
    byte_id = int.to_bytes(int_id, b, 'big')
    byte_name = int.to_bytes(int_name, b1, 'big')
    byte_surname = int.to_bytes(int_surname, b2, 'big')
    byte_ins = int.to_bytes(int_ins, b3, 'big')
    byte_date = int.to_bytes(int_date, b4, 'big')

    # We decode our bytes and finally get our encrypted string values
    id_encrypted = byte_id.decode('utf-8', errors="replace")
    name_encrypted = byte_name.decode('utf-8', errors="replace")
    surname_encrypted = byte_surname.decode('utf-8', errors="replace")
    ins_encrypted = byte_ins.decode('utf-8', errors="replace")
    date_encrypted = byte_date.decode('utf-8', errors="replace")

    # Now that we have the encrypted values, we can decrypt easily by using our xor function
    id_decrypted = xor_encrypt_decrypt(id_encrypted, doc_id)
    name_decrypted = xor_encrypt_decrypt(name_encrypted, doc_id)
    surname_decrypted = xor_encrypt_decrypt(surname_encrypted, doc_id)
    ins_decrypted = xor_encrypt_decrypt(ins_encrypted, doc_id)
    date_decrypted = xor_encrypt_decrypt(date_encrypted, doc_id)

    # And we are printing the information here
    print("\n\nThe Identification Number of The Patient is : ", id_decrypted, "\n\n")
    print("\n\nName/Surname: ", name_decrypted, "/", surname_decrypted)
    print("\n\nThe Insurance Number of The Patient is : ", ins_decrypted, "\n\n")
    print("\n\nThe Date of The Inspection was(MM/DD/YYYY) : ",
          date_decrypted[0:2], "/", date_decrypted[2:4], "/", date_decrypted[4:9])

# MAIN FUNCTION
print("\n\n\t\t\t\tWelcome to MPIE(MEDICAL PHOTO INFORMATION ENCRYPTION)!\n\n")
print("\t\t\t\t********************\n\n")
select = input("Would you like to encrypt or decrypt information?(1 for encrypt,2 for decrypt,3 to exit)")
while select != '3':
    if select == '1':
        encrypt()
        select = input("\n\nWould you like to encrypt or decrypt information?(1 for encrypt,2 for decrypt,3 to exit)")
    elif select == '2':
        decrypt()
        select = input("\n\nWould you like to encrypt or decrypt information?(1 for encrypt,2 for decrypt,3 to exit)")
exit()