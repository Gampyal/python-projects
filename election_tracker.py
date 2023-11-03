
import psycopg2

import mysql.connector

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234567890",
    database="election"
    )

myCursor = db.cursor()


# Retrive uniqueid and polling unit name from polling unit table
myCursor.execute("SELECT uniqueid, polling_unit_name FROM polling_unit")
pu_name_id_fetch = myCursor.fetchall()


# From ids, mapping each uniqueid to its polling unit name, and storing in a dictionary
pu_name_id = {id: name for id, name in pu_name_id_fetch}



# Using the polling unit unique id to find their respective data form the announced pu results table
def find_scores(polling_uuid):
  announced_pu_results_query = "SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s"

  try:
    myCursor.execute(announced_pu_results_query, (polling_uuid,)) 
    announced_pu_data = myCursor.fetchall()


    # Mapping party scores to their respective party abbreviations
    announced_pu_scores = {}
    for abbreviation, score in announced_pu_data:
      announced_pu_scores[abbreviation] = score

    return announced_pu_scores
  

  except psycopg2.Error as e:
    print("Error executing query: ", e)
    return None
  



# Using the polling unit unique id to display their respective data
def display_results(polling_uuid):
  announced_pu_results_data = find_scores(polling_uuid)
  match_found = False

  if announced_pu_results_data is not None:

    # Use the polling uuid submitted by the user to display the corresponding polling unit name
    for key, value in pu_name_id.items():
      if key == polling_uuid:
          print("\nPolling Unit Name:", value)
          match_found = True

    if not match_found:
      print("No polling unit found with ID {}.".format(polling_uuid))

    # Display party abbreviation and corresponding score  
    for abbreviation, score in announced_pu_results_data.items():
      print("{}: {}".format(abbreviation, score))
      
  else:
    print("No results found for polling unit {}.".format(polling_uuid))


# Display list of polling units and their unique IDs from which to choose
print("\nPolling units")
for id, name in pu_name_id_fetch:
    print(f'{id}. {name}')
polling_uuid = int(input('enter polling unit unique id for which to display results: '))


display_results(polling_uuid)




# Display list of LGAs and their unique IDs from which to choose
myCursor.execute("SELECT lga_id, lga_name FROM lga")
lga_list = myCursor.fetchall()
print("\nLGA Listing")
for id, name in lga_list:
    print(f'{id}. {name}')

lga_query = "SELECT lga_name FROM lga WHERE lga_id = %s;"



lga_id = input("enter lga id here for which to display results: ")


myCursor.execute(lga_query, (lga_id,))
lga_name = myCursor.fetchall()

print("\n", lga_name[0][0], "LGA Results")


# Use lga_id to retrieve polling unit unique ids with same lga_id from polling unit table
def lga(lga_id):
    query = "SELECT uniqueid FROM polling_unit WHERE lga_id = %s;"
    try:
        myCursor.execute(query, (lga_id,))
        result = myCursor.fetchall()

        return result
    
    except psycopg2.Error as e:
        print("Error reading query: ", e)
        return None
    

# Assign result of lga(lga_id) function to pu_unique_ids variable
pu_unique_ids = lga(lga_id)



if pu_unique_ids is not None:
    party_scores = {}

    # Looping through pu_unique_ids variable for each instance of polling unit unique id to select their party abbreviation and party score from announced pu results table
    for id_tuple in pu_unique_ids:
        id = id_tuple[0]
        lgaquery = "SELECT party_abbreviation, party_score FROM announced_pu_results WHERE polling_unit_uniqueid = %s"
        try:
            myCursor.execute(lgaquery, (id,))
            lga_result = myCursor.fetchall()

            # Create new instance of party abbreviations and scores, and subsequently add up all values of same abbreviations to give total result for each party abbreviation
            for abbreviation, score in lga_result:
                if abbreviation in party_scores:
                    party_scores[abbreviation] += score
                else:
                    party_scores[abbreviation] = score

        except psycopg2.Error as e:
            print("Error reading qquery: ", e)

    # Convert party scores in dictionary to list of tuples
    party_scores_list = list(party_scores.items())
    for abbreviation, score in party_scores_list:
        print(f'{abbreviation}: {score}')









# Prompt the user for input for new polling unit
print("\n To create a new polling unit, please supply the following accurately: ")
n_polling_unit_id = int(input("Enter polling unit ID: "))
n_ward_id = int(input("Enter ward ID: "))
n_lga_id = int(input("Enter LGA ID: "))
n_uniquewardid = int(input("Enter unique ward ID (or leave blank for NULL): ") or 'NULL')
n_polling_unit_number = input("Enter polling unit number (or leave blank for NULL): ") or 'NULL'
n_polling_unit_name = input("Enter polling unit name (or leave blank for NULL): ") or 'NULL'
n_polling_unit_description = input("Enter polling unit description (or leave blank for NULL): ") or 'NULL'
n_lat = input("Enter latitude (or leave blank for NULL): ") or 'NULL'
n_long = input("Enter longitude (or leave blank for NULL): ") or 'NULL'
n_entered_by_user = input("Enter user name (or leave blank for NULL): ") or 'NULL'
n_date_entered = input("Enter date entered (or leave blank for NULL in format 'YYYY-MM-DD HH:MM:SS'): ") or 'NULL'
n_user_ip_address = input("Enter user IP address (or leave blank for NULL): ") or 'NULL'

# Prepare the SQL query
sql = "INSERT INTO polling_unit (polling_unit_id, ward_id, lga_id, uniquewardid, polling_unit_number, polling_unit_name, polling_unit_description, lat, `long`, entered_by_user, date_entered, user_ip_address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# Define the values to be inserted
values = (n_polling_unit_id, n_ward_id, n_lga_id, n_uniquewardid, n_polling_unit_number, n_polling_unit_name, n_polling_unit_description, n_lat, n_long, n_entered_by_user, n_date_entered, n_user_ip_address)

try:
    # Execute the query
    myCursor.execute(sql, values)
    db.commit()
    print("\nNew polling unit created successfully!")
except Exception as e:
    print("\nFailed to create new polling unit:", e)
    db.rollback()





# Display available polling units with their unique IDs for user to choose
print("\nAvailable Polling Units and their Unique IDs:")
for id, name in pu_name_id_fetch:
    print(f'{id}. {name}')
selected_uuid = int(input("\nEnter the uniqueid you want to use: "))
def confirmed(selcted_uuid):
    if selcted_uuid in pu_name_id:
        return selected_uuid
selected_polling_unit_id = confirmed(selected_uuid)


# Get party abbreviations (with maximum length of 4 characters)
myCursor.execute("SELECT partyname FROM party")
party_abbreviations = [result[0][:4] for result in myCursor.fetchall()]


# Prompt user for party scores
party_scores = {}
for party_abbr in party_abbreviations:
    score = int(input(f"Enter score for {party_abbr}: "))
    party_scores[party_abbr] = score


pu_results_entered_by_user = input("\nEnter user name (or leave blank for NULL): ") or 'NULL'
pu_results_date_entered = input("Enter date entered (or leave blank for NULL in format 'YYYY-MM-DD HH:MM:SS'): ") or 'NULL'
pu_results_user_ip_address = input("Enter user IP address (or leave blank for NULL): ") or 'NULL'


# Generate and Execute INSERT Queries
for party_abbr, score in party_scores.items():
    insert_query = f"INSERT INTO announced_pu_results (polling_unit_uniqueid, party_abbreviation, party_score, entered_by_user, date_entered, user_ip_address) VALUES ({selected_polling_unit_id}, '{party_abbr}', {score}, '{pu_results_entered_by_user}', '{pu_results_date_entered}', '{pu_results_user_ip_address}')"
    try:
        # Execute the query
        myCursor.execute(insert_query)
        db.commit()
        found = False
        # Use the polling uuid submitted by the user to display the corresponding polling unit name
        for key, value in pu_name_id.items():
            if key == selected_polling_unit_id:
                print("\nResults for", value, "added successfully!")
                found = True

            if not found:
                print("\nNo polling unit found with ID {}.".format(selected_polling_unit_id))
    except Exception as e:
        print(f"\nFailed to upload results for", {selected_polling_unit_id},  e)
        db.rollback()
    




myCursor.close()
db.close()