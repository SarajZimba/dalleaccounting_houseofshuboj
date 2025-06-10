# import os
# import django

# # Set the settings module for Django
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "root.settings")  # Change this!

# # Setup Django
# django.setup()
# import pandas as pd
# from user.models import Customer

# def import_customers_from_excel(excel_file_path):
#     # Read the Excel file
#     df = pd.read_excel(excel_file_path)
    
#     # Ensure column names match your Excel file
#     df.columns = ['fname', 'lname', 'section', 'roll_num']

    
#     customers_created = 0
    
#     for index, row in df.iterrows():
#         # Clean the data (remove extra spaces)
#         first_name = str(row['fname']).strip()
#         last_name = str(row['lname']).strip()
#         section = str(row['section']).strip()
        
#         # Concatenate first and last name for the name field
#         full_name = f"{first_name} {last_name}"
        
#         # Create the customer
#         try:
#             customer = Customer.objects.create(
#                 name=full_name,
#                 section=section,
#                 # You can add more fields here if needed
#             )
#             customers_created += 1
#             print(f"Created customer: {full_name} (Section: {section})")
#         except Exception as e:
#             print(f"Error creating customer {full_name}: {str(e)}")
    
#     print(f"\nSuccessfully created {customers_created} customers out of {len(df)} records.")

# # Example usage:
# if __name__ == "__main__":
#     # Set these values appropriately before running
#     excel_path = "Class_11.xlsx"  # Update this path
    
#     import_customers_from_excel(
#         excel_path
#     )