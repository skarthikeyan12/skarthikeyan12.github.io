if request.method == 'POST':
        property_type = request.form['property_type']
        conn = sqlite3.connect(PATH_TO_DB)
        cursor = conn.cursor()

        query = "SELECT p.property_id, t.property_name FROM property AS p LEFT OUTER JOIN property_type AS t ON p.property_type = t.property_type;"
        property_info = pd.read_sql_query(query, conn, params = (property_type,))

        conn.close()

        if property_info is None:
            message = 'Property with id {} does not exist.'.format(property_type)
            return render_template('find_property.html', message=message)
        else:
            return render_template('find_property.html', property_info = property_info.to_html(index = False))
    else:
        return render_template('find_property.html')