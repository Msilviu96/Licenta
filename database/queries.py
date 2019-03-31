from .models import Child, Device

queries = {
    'get_child_by_device_token': """SELECT c.*
                                     FROM database_child c
                                     JOIN database_device d
                                     ON c.id = d.child_id
                                     WHERE d.token = '{}'""",
}



