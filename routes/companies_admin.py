from flask import request, redirect, render_template, session, flash, url_for
import re
from server import app
from db import get_data_connection
import html

@app.route('/admin/companies')
def admin_list_companies():
    if session.get('role') != 'admin':
        return "Access denied", 403
    conn = get_data_connection()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return render_template('admin/admin_companies.html', companies=companies)

@app.route('/admin/companies/add', methods=['GET', 'POST'])
def admin_add_company():
    if session.get('role') != 'admin':
        return "Access denied", 403
    if request.method == 'POST':
        company_name = request.form['company_name'].strip()
        owner = request.form['owner'].strip()
        if not company_name or not owner:
            flash("Campos obligatorios")
            return render_template(
                'admin/admin_companies.html',
                company_name=company_name,
                owner=owner
            )

        if len(company_name) > 100 or not re.match(r'^[\w\s\-]+$', company_name):
            flash("Nombre de compañía no válido")
            return render_template('admin/admin_companies.html', company_name=company_name, owner=owner,)
        
        if len(company_name) > 100 or not re.match(r'^[A-Za-z\s]+$', owner):
            flash("Nombre del propietario inválido")
            return render_template('admin/admin_companies.html', company_name=company_name, owner=owner)
        
        company_name = html.escape(company_name)
        owner = html.escape(owner)
        conn = get_data_connection()
        #conn.execute("INSERT INTO companies (name, owner) VALUES ('"+ company_name+"', '"+owner+"')")
        conn.execute(
            "INSERT INTO companies (name, owner) VALUES (?, ?)",
            (company_name, owner)
        )
        conn.commit()
        conn.close()
        return redirect('/admin/companies')
    return render_template('admin/admin_companies.html')

@app.route('/admin/companies/delete', methods=['POST'])
def delete_company():
    #if session.get('role') != 'admin':
    #    return "Access denied", 403
    #company = request.form['company']
    company_id = request.form.get('company')
    
    if not company_id or not company_id.isdigit():
        return "Invalid company ID", 400
    
    conn = get_data_connection()

    # Validar que la compañía exista
    company = conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
    if not company:
        conn.close()
        return "Company not found", 404
    
    # Solo admin puede eliminar
    if session.get('role') != 'admin':
        conn.close()
        return "Access denied", 403

    conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
    conn.execute("DELETE FROM comments WHERE company_id = ?", (company_id,))
    #conn.execute("DELETE FROM companies WHERE id = "+ company)
    #conn.execute("DELETE FROM comments WHERE company_id = " + company)
    conn.commit()
    conn.close()
    return redirect('/admin/companies')