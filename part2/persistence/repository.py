class InMemoryRepository:
    def __init__(self):
        self.storage = {}

    def add(self, obj):
        self.storage[obj.id] = obj

    def get(self, obj_id):
        return self.storage.get(obj_id)

    def all(self):
        return list(self.storage.values())

    def delete(self, obj_id):
        if obj_id in self.storage:
            del self.storage[obj_id]
