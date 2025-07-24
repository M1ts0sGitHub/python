import string, random

#Map of characters for English and Greek
charmap = string.ascii_letters + string.digits + string.punctuation + " αβγδεζηθικλμνξοπρςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"

#Encrypt single text - password
def encrypt(plain_text,password):
    encrypted_text = ""
    for i, char in enumerate(plain_text):
        if char in charmap:
            encrypted_text += charmap[(charmap.index(char) + charmap.index(password[i % len(password)]) + i) % len(charmap)]
        else:
            encrypted_text += char
    return encrypted_text

#Decrypt single text - password
def decrypt(cipher_text,password):
    decrypted_text = ""
    for i, char in enumerate(cipher_text):
        if char in charmap:
            decrypted_text += charmap[(charmap.index(char) - charmap.index(password[i % len(password)]) - i) % len(charmap)]
        else:
            decrypted_text += char
    return decrypted_text

#Encrypt multiple texts | Passwords are auto generated and given
def multiple_encrypt(list_of_plain_texts):
    encrypted_list_of_texts = []
    max_len_of_texts = max(len(text) for text in list_of_plain_texts)
    for i in range(len(list_of_plain_texts)):
        list_of_plain_texts[i] = list_of_plain_texts[i] + (max_len_of_texts - len(list_of_plain_texts[i]))*"E"        
    password = "".join(random.choice(charmap) for i in range(max_len_of_texts))
    for text in list_of_plain_texts:
        encrypted_list_of_texts.append(encrypt(text, password))
    return password, encrypted_list_of_texts

#Decrypt texts created with multiple_encrypt
def multiple_decrypt(cipher_text, password):
    decrypted_text = ""
    for i, char in enumerate(password):
        if char in charmap:
            decrypted_text += charmap[(charmap.index(char) - charmap.index(cipher_text[i % len(cipher_text)]) - i) % len(charmap)]
        else:
            decrypted_text += char
    return decrypted_text.replace("E", "")



### Prouf of consept ###
## Single Encryption ##
print('\nSingle Encryption\n')
plain_text = "plain_text"
password ="password"
encrypted_text = encrypt(plain_text,password)
decrypted_text = decrypt(encrypted_text,password)
print(f'Encrypting this plain text "{plain_text}" with this password "{password}" we get this encrypted cipher "{encrypted_text}"')
print(f'which decrypted is "{decrypted_text}"\n')




## Multiple Encryption ##
multiple_texts = ["Hello world", "My name is Dimitris"]
print('Multiple Encryption\n')
for i in range(len(multiple_texts)):
    print(f'Text {i+1}: {multiple_texts[i]}')

#Encrypt multiple texts to one encrypted text. Compute different passwords in order to decrypt the original message
encrypted_text, passwords = multiple_encrypt(multiple_texts)

print(f'Encrypted Text: {encrypted_text}')
for i in range(len(passwords)):
    print(f'Password {i+1}: {passwords[i]}')
    
for i in range(len(passwords)):
    print(f'Encrypted text "{encrypted_text}" decrypts with password "{passwords[i]}" to the original message "{multiple_decrypt(encrypted_text,passwords[i])}"')