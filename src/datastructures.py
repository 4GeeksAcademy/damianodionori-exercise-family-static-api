from random import randint


class FamilyStructure:
    def __init__(self, last_name):
        self.last_name = last_name

        self._members = [
            {
                "id": self._generate_id(),
                "first_name": "John",
                "last_name": self.last_name,
                "age": 33,
                "lucky_numbers": [7, 13, 22],
            },
            {
                "id": self._generate_id(),
                "first_name": "Jane",
                "last_name": self.last_name,
                "age": 35,
                "lucky_numbers": [10, 14, 3],
            },
            {
                "id": self._generate_id(),
                "first_name": "Jimmy",
                "last_name": self.last_name,
                "age": 5,
                "lucky_numbers": [1],
            },
        ]

    def _generate_id(self):
        return randint(0, 100)

    def add_member(self, member):
        inner_member = {
            "first_name": member["first_name"],
            "last_name": self.last_name,
            "age": member["age"],
            "lucky_numbers": member["lucky_numbers"],
            "id": self._generate_id(),
        }
        self._members.append(inner_member)
        return inner_member

    def delete_member(self, member_id):
        member_to_delete = self.get_member(member_id)
        self._members.remove(member_to_delete)

        return {"message": "Member deleted successfully"}

    def get_member(self, member_id):
        for member in self._members:
            if member["id"] == member_id:
                print(member)
                return member
        return None
    
    def update_member(self, member_id, updated_member):
        for i, member in enumerate(self._members):
            if member["id"] == member_id:
                for key, value in updated_member.items():
                    if key in self._members[i]:
                        self._members[i][key] = value
                return {"message": "Member updated successfully", "updated_member": updated_member}

        return {"error": "Member not found"}

    def get_all_members(self):
        return self._members
