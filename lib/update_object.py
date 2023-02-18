from flask import jsonify

def update_object(object, data):
  fields = data.keys()

  for field in fields:
    try:
        getattr(object, field)
        setattr(object, field, data[field])
    except AttributeError:
        return jsonify({'ERROR': f'Record has no attribute: {field}'}), 400