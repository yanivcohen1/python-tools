from flask import Blueprint
from flask import session
from flask import request
from flask_jsonpify import jsonify

bp = Blueprint("employees", __name__, url_prefix="/employees")
employeess = {'employees': [{'id':1, 'name':'Balram'},{'id':2, 'name':'Tom'}]}
#for seralization use cast-class-json-class.py
#see for mysql + rest - rest_crud_mysql folder
@bp.route("/") #, methods=("GET", "POST", "PUT", "DELETE")
def employees():
    """Clear the current session, including the stored user id."""
    #for GET
    #user_id = session.get("user_id")
    #for POST
    #username = request.form["username"]
    #for PUT
    #_json = request.json
	#_id = _json['id']
    #for DELETE
    #@app.route('/delete/<int:id>', methods=['DELETE'])
    #def delete_user(id):
    return employeess

@bp.route("/<employee_id>")
def get(employee_id):
        print('Employee id:' + employee_id)
        result = employeess["employees"][int(employee_id)-1]["name"] #{'data': {'id':employee_id, 'name':'Balram1'}}
        #send as mimetype='application/json'
        return jsonify(result) # str(result)
        # to change the return status 
        # response = app.response_class(
        # response=json.dumps(data),
        # status=200,
        # mimetype='application/json'
    )
    return response