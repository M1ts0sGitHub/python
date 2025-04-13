import DB_Lite

db = DB_Lite.Database('Phonebook.db')
db.delete_table('Phonebook')
db.create_table('Phonebook', '"First Name" TEXT, "Last Name" TEXT, CellPhone INTEGER')

# Add Data
db.insert_into_table('Phonebook', '("Δημήτρης", "Αλεξανδρόπουλος", 6981188658)')
db.insert_into_table('Phonebook', '("Λένα", "Νικολαΐδου", 6983460228)')
db.insert_into_table('Phonebook', '("Παύλος", "Αλεξανδρόπουλος", 6972631869)')
db.insert_into_table('Phonebook', '("Ζανέτ", "Γκίκα", 6980462020)')

# Print Table
db.print_table('Phonebook')