import threading


_thread_locals = threading.local()

def set_current_user(user):
    _thread_locals.user=user

def get_current_user():
    return getattr(_thread_locals, 'user', None)



class UtilModel:
    def save_model(self, request, obj, form, change):
        if obj.created_by == None:
            obj.created_by = request.user
        #super().save_model(request, obj, form, change)
        obj.modified_by = request.user
        super().save_model(request, obj, form, change)
