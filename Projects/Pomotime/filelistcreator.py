import os, hashlib, keyboard

def generate_integrity_file():
    with open("filelist.txt", "w") as f:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file == "filelist.txt":
                    pass
                else:
                    file_path = os.path.join(root, file)
                    with open(file_path, 'rb') as fp:
                        f.write(file_path + "," + hashlib.md5(fp.read()).hexdigest() + "\n")
                
def check_integrity(filelist):
    with open(filelist, "r") as f:
        for line in f:
            file_path, correct_hash = line.strip().split(",")
            # check if the hashes are correct
            with open(file_path, 'rb') as fp:
                accual_hash = hashlib.md5(fp.read()).hexdigest()
                if accual_hash == correct_hash:
                    print(f"{file_path} is valid")
                else:
                    print(f"{file_path} is not valid. Correct hash: {correct_hash}, Actual hash: {accual_hash}")
        
generate_integrity_file()
check_integrity('./filelist.txt')

print('Press "q" to exit')
keyboard.wait('q')