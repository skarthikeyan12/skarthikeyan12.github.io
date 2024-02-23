from flask import Flask, render_template, request, url_for
import sqlite3
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
import base64
import pandas as pd
import os

PARENT_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

PATH_TO_DB = os.path.join(PARENT_DIR, "real_estate.db")

@app.route('/')

@app.route('/home')
def home():
    return render_template('home_page.html')
#
#
#Add Property
#
#
@app.route('/add_property', methods=['GET', 'POST'])
def add_property():
    if request.method == 'POST':
        property_type = request.form.get('property_type')
        property_price = request.form.get('property_price')
        property_square_footage = request.form.get('property_square_footage')
        property_bed = request.form.get('property_bed')
        property_bath = request.form.get('property_bath')
        monthly_cost = request.form.get('monthly_cost')
        property_unit = request.form.get('property_unit')
        property_number = request.form.get('property_number')
        property_street = request.form.get('property_street')
        property_zipcode = request.form.get('property_zipcode')

        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(property_id) FROM property;")
        max_property_id = cursor.fetchone()[0]

        if max_property_id is None:
            property_id = 1
        else:
            property_id = max_property_id + 1

        cursor.execute("INSERT INTO property (property_id, property_type,\
                        property_price, property_square_footage, property_bed,\
                        property_bath, monthly_cost, property_unit, property_number,\
                        property_street, property_zipcode)\
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", \
                       (property_id, property_type, property_price, property_square_footage,
                        property_bed, property_bath, monthly_cost, property_unit,
                        property_number, property_street, property_zipcode))

        conn.commit()
        conn.close()  # Corrected the closing of the connection

        return '<h1>Success!</h1> The property record has been successfully added to the database.'
    else:
        return render_template('adding_property.html')   
#
#
#Find Property  DONE
#
#    

@app.route('/find_property', methods=['GET', 'POST'])
def find_property():
    if request.method == 'POST' and "find_property" in request.form:
        property_type = request.form.get('property_type')
        
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT p.property_id, t.property_name FROM property AS p LEFT OUTER JOIN \
            property_type AS t ON p.property_type = t.property_type WHERE p.property_type=?", (property_type,))
        property_info = cursor.fetchall()
        conn.close()

        return render_template('find_property.html', property_info=property_info)
    else:
        return render_template('find_property.html')

#
#
# See Listings DONE
#
#
def create_property_chart(data: list) -> str:
    Properties = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    plt.figure(figsize=(8,6))
    plt.bar(Properties, counts, color=['blue', 'red', 'green', 'purple'])
    plt.xlabel('Property Types')
    plt.ylabel('Count')
    plt.title('Property Type Distribution')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{image_base64}"

@app.route('/see_listings', methods=['GET', 'POST'])
def see_listings():
    if not request.method == "POST":
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        cursor.execute ("SELECT * FROM property ORDER BY property_price DESC;")
        property_info = cursor.fetchall()
        conn.close()
        
        return render_template('see_listings.html', property_info = property_info)
    
    if "find_property" in request.form:
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT property_type, COUNT(*) FROM property GROUP BY property_type")
        property_data = cursor.fetchall()
        conn.close()
        
        return render_template ('BAR_find_property.html', chart_image=create_property_chart(property_data))

    return "Error"
#
# 
# Bar Graph for Amentities
#
#  
def create_amentity_chart(data: list) -> str:
    amentities = [row[0] for row in data]
    counts = [row[1] for row in data]
    
    plt.figure(figsize=(8,6))
    plt.bar(amentities, counts, color=['blue', 'red', 'green', 'orange', 'purple'])
    plt.xlabel('Amenity')
    plt.ylabel('Count')
    plt.title('Property Amentity Distribution')
    
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{image_base64}"

#
# 
# Add Amentity
#
#
@app.route('/add_amentity', methods=['GET', 'POST'])
def add_amentity():
    if not request.method == "POST":
        return render_template ('find_amentity.html')  
    
    if "add_amentity" in request.form:
        amentity_name = request.form.get('amentity_name')
        
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        
        cursor.execute ("SELECT MAX(amentity_id) FROM amentity")
        max_amentity_id = cursor.fetchone()[0]

        if max_amentity_id is None:
            amentity_id = 1
        else:
            amentity_id = max_amentity_id + 1
        
        cursor.execute("INSERT INTO amentity (amentity_id, amentity_name)\
        VALUES (?, ?)", \
        (amentity_id, amentity_name,))
        
        conn.commit()
        
        conn.close
        
        return ('<h2> Success!</h2> The amentity has been \
        successfully added to the database.')
    
    if "find_amentity" in request.form:
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        
        cursor.execute("SELECT amentity_id, COUNT(*) FROM property_amentity GROUP BY amentity_id")
        property_amentity_data = cursor.fetchall()
        
        conn.close()
        
        return render_template ('BAR_find_amentity.html', chart_image=create_amentity_chart(property_amentity_data))

    return "Error"

#
# 
# Find Realtor  HELP
#
#     
@app.route('/find_realtor', methods=['GET', 'POST'])
def find_realtor():
    
    if not request.method == "POST":
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM realtor ORDER BY realtor_last_name ASC;")
        rows=cursor.fetchall()

        return render_template('find_realtor.html', rows=rows)
    
    if request.method == 'POST':
        realtor_id = request.form.getlist('realtor_id')
        
        if realtor_id:
            conn = sqlite3.connect(PATH_TO_DB)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM realtor_showings WHERE realtor_id=?", (realtor_id))
            realtor_data=cursor.fetchall()
            
            conn.close()

        return render_template('find_realtor.html', realtor_data=realtor_data)
    
    return render_template('find_realtor.html')
    
if __name__ == '__main__':
    app.run(debug=True)
